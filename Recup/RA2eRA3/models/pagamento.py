from models.db import db
from datetime import datetime

class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    comanda_id = db.Column(db.Integer, db.ForeignKey('comandas.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)  # 'dinheiro', 'cartao_credito', 'cartao_debito', 'pix'
    status = db.Column(db.String(20), nullable=False, default='pendente')  # 'pendente', 'aprovado', 'cancelado'
    processado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    observacoes = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    processado_at = db.Column(db.DateTime)
    
    # Relacionamentos
    comanda = db.relationship('Comanda', back_populates='pagamentos')
    processado_por = db.relationship('Usuario', foreign_keys=[processado_por_id])
    
    def __init__(self, comanda_id, valor, forma_pagamento, observacoes=None):
        self.comanda_id = comanda_id
        self.valor = valor
        self.forma_pagamento = forma_pagamento
        self.status = 'pendente'
        self.observacoes = observacoes
    
    @staticmethod
    def create_pagamento(comanda_id, valor, forma_pagamento, observacoes=None):
        """Criar um novo registro de pagamento"""
        try:
            from models.comanda import Comanda
            
            # Verificar se a comanda existe e está fechada
            comanda = Comanda.get_comanda(comanda_id)
            if not comanda:
                return False, "Comanda não encontrada"
            
            if comanda.status == 'aberta':
                return False, "A comanda precisa estar fechada para processar o pagamento"
            
            if comanda.status == 'paga':
                return False, "Esta comanda já foi paga"
            
            # Verificar se o valor está correto
            if valor != comanda.valor_total:
                return False, f"Valor do pagamento (R$ {valor:.2f}) não corresponde ao total da comanda (R$ {comanda.valor_total:.2f})"
            
            pagamento = Pagamento(
                comanda_id=comanda_id,
                valor=valor,
                forma_pagamento=forma_pagamento,
                observacoes=observacoes
            )
            db.session.add(pagamento)
            db.session.commit()
            
            return True, pagamento
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def processar_pagamento(pagamento_id, usuario_id, aprovar=True):
        """Processar o pagamento (aprovar ou cancelar) - apenas caixa pode fazer isso"""
        try:
            from models.comanda import Comanda
            
            pagamento = Pagamento.query.get(pagamento_id)
            if not pagamento:
                return False, "Pagamento não encontrado"
            
            if pagamento.status != 'pendente':
                return False, f"Este pagamento já foi {pagamento.status}"
            
            pagamento.status = 'aprovado' if aprovar else 'cancelado'
            pagamento.processado_por_id = usuario_id
            pagamento.processado_at = datetime.now()
            
            # Se aprovado, marcar a comanda como paga
            if aprovar:
                comanda = Comanda.get_comanda(pagamento.comanda_id)
                sucesso, resultado = comanda.marcar_como_paga()
                if not sucesso:
                    db.session.rollback()
                    return False, resultado
            
            db.session.commit()
            return True, pagamento
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_pagamentos():
        """Listar todos os pagamentos"""
        return Pagamento.query.order_by(Pagamento.created_at.desc()).all()
    
    @staticmethod
    def get_pagamentos_pendentes():
        """Listar pagamentos pendentes"""
        return Pagamento.query.filter_by(status='pendente').order_by(Pagamento.created_at.desc()).all()
    
    @staticmethod
    def get_pagamentos_by_comanda(comanda_id):
        """Listar pagamentos de uma comanda específica"""
        return Pagamento.query.filter_by(comanda_id=comanda_id).all()
    
    @staticmethod
    def get_pagamento(pagamento_id):
        """Buscar um pagamento específico"""
        return Pagamento.query.get(pagamento_id)
    
    def __repr__(self):
        return f'<Pagamento R$ {self.valor:.2f} - {self.forma_pagamento} - {self.status}>'
