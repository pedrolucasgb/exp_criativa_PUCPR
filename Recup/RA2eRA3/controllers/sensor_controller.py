from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.itens_cardapio import ItemCardapio
from models.comanda import Comanda
from models.item_comanda import ItemComanda

sensor_bp = Blueprint("cardapio", __name__)

@sensor_bp.route("/")
@login_required
def cardapio():
    """Ver cardápio"""
    itens = ItemCardapio.get_itens_disponiveis()
    return render_template("cardapio.html", itens=itens)

@sensor_bp.route("/abrir_comanda", methods=["POST"])
@login_required
def abrir_comanda():
    """Abrir nova comanda"""
    try:
        numero_mesa = request.form.get("numero_mesa")
        
        if not numero_mesa:
            flash("Número da mesa é obrigatório.", "error")
            return redirect(url_for("auth.dashboard"))
        
        # Atendente e caixa devem selecionar um cliente
        if current_user.is_atendente() or current_user.is_caixa():
            cliente_id = request.form.get("cliente_id")
            if not cliente_id:
                flash("Você deve selecionar um cliente.", "error")
                return redirect(url_for("auth.dashboard"))
            cliente_id = int(cliente_id)
        else:
            cliente_id = current_user.id
        
        success, comanda = Comanda.save_comanda(int(numero_mesa), cliente_id)
        
        if success:
            flash(f"Comanda #{comanda.id} aberta para mesa {numero_mesa}!", "success")
        else:
            flash(f"Erro ao abrir comanda: {comanda}", "error")
    except Exception as e:
        flash(f"Erro: {str(e)}", "error")
    
    return redirect(url_for("auth.dashboard"))

@sensor_bp.route("/adicionar_item", methods=["POST"])
@login_required
def adicionar_item():
    """Adicionar item à comanda"""
    try:
        comanda_id = request.form.get("comanda_id")
        item_id = request.form.get("item_id")
        quantidade = request.form.get("quantidade", 1)
        
        # Verificar se a comanda existe
        comanda = Comanda.get_comanda(int(comanda_id))
        if not comanda:
            flash("Comanda não encontrada.", "error")
            return redirect(url_for("auth.dashboard"))
        
        # Validar status da comanda
        if comanda.status == 'paga':
            flash("Não é possível adicionar itens a uma comanda paga.", "error")
            return redirect(url_for("auth.dashboard"))
        
        # Atendente só pode adicionar em comandas abertas, caixa pode em abertas e fechadas
        if current_user.is_atendente() and comanda.status != 'aberta':
            flash("Atendentes só podem adicionar itens em comandas abertas.", "error")
            return redirect(url_for("auth.dashboard"))
        
        # Cliente só pode adicionar em sua própria comanda
        # Atendente e caixa podem adicionar em qualquer comanda
        if current_user.is_cliente() and comanda.cliente_id != current_user.id:
            flash("Você só pode modificar suas próprias comandas.", "error")
            return redirect(url_for("auth.dashboard"))
        
        # Buscar item do cardápio
        item = ItemCardapio.get_item(int(item_id))
        if not item:
            flash("Item não encontrado.", "error")
            return redirect(url_for("cardapio.cardapio"))
        
        # Adicionar à comanda
        success, result = ItemComanda.add_item_to_comanda(
            int(comanda_id),
            int(item_id),
            int(quantidade),
            item.preco
        )
        
        if success:
            flash(f"{quantidade}x {item.nome} adicionado à comanda!", "success")
        else:
            flash(f"Erro: {result}", "error")
    except Exception as e:
        flash(f"Erro: {str(e)}", "error")
    
    return redirect(url_for("auth.dashboard"))

@sensor_bp.route("/fechar_comanda/<int:comanda_id>", methods=["POST"])
@login_required
def fechar_comanda(comanda_id):
    """Fechar comanda - apenas atendente e caixa"""
    try:
        # Verificar permissão
        if current_user.is_cliente():
            flash("Apenas atendente ou caixa podem fechar comandas.", "error")
            return redirect(url_for("auth.dashboard"))
        
        comanda = Comanda.get_comanda(comanda_id)
        if not comanda:
            flash("Comanda não encontrada.", "error")
            return redirect(url_for("auth.dashboard"))
        
        success, result = comanda.fechar_comanda()
        
        if success:
            flash(f"Comanda #{comanda_id} fechada! Total: R$ {result.valor_total:.2f}", "success")
        else:
            flash(f"Erro: {result}", "error")
    except Exception as e:
        flash(f"Erro: {str(e)}", "error")
    
    return redirect(url_for("auth.dashboard"))

@sensor_bp.route("/editar_item/<int:item_id>", methods=["POST"])
@login_required
def editar_item(item_id):
    """Editar quantidade de item da comanda - apenas atendente e caixa"""
    try:
        # Verificar permissão
        if current_user.is_cliente():
            flash("Apenas atendente ou caixa podem editar itens.", "error")
            return redirect(url_for("auth.dashboard"))
        
        from models.item_comanda import ItemComanda
        item = ItemComanda.get_item_comanda(item_id)
        
        if not item:
            flash("Item não encontrado.", "error")
            return redirect(url_for("auth.dashboard"))
        
        comanda = Comanda.get_comanda(item.comanda_id)
        
        # Caixa pode editar comandas fechadas, atendente só abertas
        if current_user.is_atendente() and comanda.status != 'aberta':
            flash("Atendentes só podem editar itens de comandas abertas.", "error")
            return redirect(url_for("auth.dashboard"))
        
        if comanda.status == 'paga':
            flash("Não é possível editar itens de comandas pagas.", "error")
            return redirect(url_for("auth.dashboard"))
        
        # Obter nova quantidade
        nova_quantidade = request.form.get("quantidade")
        if not nova_quantidade or int(nova_quantidade) < 1:
            flash("Quantidade inválida.", "error")
            return redirect(url_for("auth.dashboard"))
        
        success, result = ItemComanda.update_item_comanda(item_id, int(nova_quantidade))
        
        if success:
            flash("Quantidade atualizada com sucesso.", "success")
        else:
            flash(f"Erro ao atualizar item: {result}", "error")
    except Exception as e:
        flash(f"Erro: {str(e)}", "error")
    
    return redirect(url_for("auth.dashboard"))

@sensor_bp.route("/remover_item/<int:item_id>", methods=["POST"])
@login_required
def remover_item(item_id):
    """Remover item da comanda - apenas atendente e caixa"""
    try:
        # Verificar permissão
        if current_user.is_cliente():
            flash("Apenas atendente ou caixa podem remover itens.", "error")
            return redirect(url_for("auth.dashboard"))
        
        from models.item_comanda import ItemComanda
        item = ItemComanda.get_item_comanda(item_id)
        
        if not item:
            flash("Item não encontrado.", "error")
            return redirect(url_for("auth.dashboard"))
        
        comanda_id = item.comanda_id
        comanda = Comanda.get_comanda(comanda_id)
        
        # Caixa pode remover de comandas fechadas, atendente só de abertas
        if current_user.is_atendente() and comanda.status != 'aberta':
            flash("Atendentes só podem remover itens de comandas abertas.", "error")
            return redirect(url_for("auth.dashboard"))
        
        if comanda.status == 'paga':
            flash("Não é possível remover itens de comandas pagas.", "error")
            return redirect(url_for("auth.dashboard"))
        
        success, result = ItemComanda.remove_item_from_comanda(item_id)
        
        if success:
            # Recalcular total da comanda
            comanda.calcular_total()
            flash("Item removido com sucesso.", "success")
        else:
            flash(f"Erro ao remover item: {result}", "error")
    except Exception as e:
        flash(f"Erro: {str(e)}", "error")
    
    return redirect(url_for("auth.dashboard"))

@sensor_bp.route("/processar_pagamento/<int:comanda_id>", methods=["POST"])
@login_required
def processar_pagamento(comanda_id):
    """Processar pagamento - apenas caixa"""
    try:
        # Verificar permissão
        if not current_user.is_caixa():
            flash("Apenas o caixa pode processar pagamentos.", "error")
            return redirect(url_for("auth.dashboard"))
        
        comanda = Comanda.get_comanda(comanda_id)
        if not comanda:
            flash("Comanda não encontrada.", "error")
            return redirect(url_for("auth.dashboard"))
        
        if comanda.status != 'fechada':
            flash("Apenas comandas fechadas podem ser pagas.", "error")
            return redirect(url_for("auth.dashboard"))
        
        forma_pagamento = request.form.get("forma_pagamento", "dinheiro")
        
        # Criar e processar pagamento
        from models.pagamento import Pagamento
        
        success, pagamento = Pagamento.create_pagamento(
            comanda_id=comanda_id,
            valor=comanda.valor_total,
            forma_pagamento=forma_pagamento
        )
        
        if not success:
            flash(f"Erro ao criar pagamento: {pagamento}", "error")
            return redirect(url_for("auth.dashboard"))
        
        # Processar (aprovar) pagamento
        success, result = Pagamento.processar_pagamento(
            pagamento_id=pagamento.id,
            usuario_id=current_user.id,
            aprovar=True
        )
        
        if success:
            flash(f"Pagamento processado! Comanda #{comanda_id} paga.", "success")
        else:
            flash(f"Erro ao processar pagamento: {result}", "error")
    except Exception as e:
        flash(f"Erro: {str(e)}", "error")
    
    return redirect(url_for("auth.dashboard"))
