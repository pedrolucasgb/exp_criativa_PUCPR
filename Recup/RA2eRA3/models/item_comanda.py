from models.db import db

class ItemComanda(db.Model):
    __tablename__ = 'itens_comanda'
    
    id = db.Column(db.Integer, primary_key=True)
    comanda_id = db.Column(db.Integer, db.ForeignKey('comandas.id'), nullable=False)
    item_cardapio_id = db.Column(db.Integer, db.ForeignKey('itens_cardapio.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    observacoes = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relacionamentos
    comanda = db.relationship('Comanda', back_populates='itens')
    item_cardapio = db.relationship('ItemCardapio', back_populates='itens_comanda')
    
    def __init__(self, comanda_id, item_cardapio_id, quantidade, preco_unitario):
        self.comanda_id = comanda_id
        self.item_cardapio_id = item_cardapio_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.subtotal = quantidade * preco_unitario
        self.observacoes = None
    
    @staticmethod
    def add_item_to_comanda(comanda_id, item_cardapio_id, quantidade, preco_unitario):
        """Adicionar um item à comanda"""
        try:
            from models.comanda import Comanda
            
            # Verificar se a comanda está aberta ou fechada (não paga)
            comanda = Comanda.get_comanda(comanda_id)
            if not comanda:
                return False, "Comanda não encontrada"
            
            if comanda.status == 'paga':
                return False, "Não é possível adicionar itens a uma comanda paga"
            
            item_comanda = ItemComanda(
                comanda_id=comanda_id,
                item_cardapio_id=item_cardapio_id,
                quantidade=quantidade,
                preco_unitario=preco_unitario
            )
            db.session.add(item_comanda)
            db.session.commit()
            
            # Recalcular o total da comanda
            comanda.calcular_total()
            
            return True, item_comanda
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_itens_by_comanda(comanda_id):
        """Listar todos os itens de uma comanda"""
        return ItemComanda.query.filter_by(comanda_id=comanda_id).all()
    
    @staticmethod
    def get_item_comanda(item_id):
        """Buscar um item específico"""
        return ItemComanda.query.get(item_id)
    
    @staticmethod
    def update_item_comanda(item_id, quantidade):
        """Atualizar quantidade de um item da comanda"""
        try:
            from models.comanda import Comanda
            
            item = ItemComanda.query.get(item_id)
            if not item:
                return False, "Item não encontrado"
            
            # Verificar se a comanda permite edição (não pode ser paga)
            comanda = Comanda.get_comanda(item.comanda_id)
            if comanda.status == 'paga':
                return False, "Não é possível editar itens de uma comanda paga"
            
            item.quantidade = quantidade
            item.subtotal = quantidade * item.preco_unitario
            
            db.session.commit()
            
            # Recalcular o total da comanda
            comanda.calcular_total()
            
            return True, item
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def delete_item_comanda(item_id):
        """Remover um item da comanda"""
        try:
            from models.comanda import Comanda
            
            item = ItemComanda.query.get(item_id)
            if not item:
                return False, "Item não encontrado"
            
            # Verificar se a comanda permite edição (não pode ser paga)
            comanda = Comanda.get_comanda(item.comanda_id)
            if comanda.status == 'paga':
                return False, "Não é possível remover itens de uma comanda paga"
            
            comanda_id = item.comanda_id
            
            db.session.delete(item)
            db.session.commit()
            
            # Recalcular o total da comanda
            comanda.calcular_total()
            
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def remove_item_from_comanda(item_id):
        """Alias para delete_item_comanda"""
        return ItemComanda.delete_item_comanda(item_id)
    
    def __repr__(self):
        return f'<ItemComanda {self.quantidade}x - R$ {self.subtotal}>'
