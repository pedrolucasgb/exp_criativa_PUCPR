from models.db import db

class ItemCardapio(db.Model):
    __tablename__ = 'itens_cardapio'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    categoria = db.Column(db.String(50), nullable=False)  # 'bebida', 'comida', 'sobremesa'
    preco = db.Column(db.Float, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relacionamentos
    itens_comanda = db.relationship('ItemComanda', back_populates='item_cardapio', lazy=True)
    
    def __init__(self, nome, descricao, categoria, preco, disponivel=True):
        self.nome = nome
        self.descricao = descricao
        self.categoria = categoria
        self.preco = preco
        self.disponivel = disponivel
    
    @staticmethod
    def save_item(nome, descricao, categoria, preco, disponivel=True):
        """Salvar um novo item do cardápio"""
        try:
            item = ItemCardapio(
                nome=nome,
                descricao=descricao,
                categoria=categoria,
                preco=preco,
                disponivel=disponivel
            )
            db.session.add(item)
            db.session.commit()
            return True, item
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_itens():
        """Listar todos os itens do cardápio"""
        return ItemCardapio.query.all()
    
    @staticmethod
    def get_itens_disponiveis():
        """Listar apenas itens disponíveis"""
        return ItemCardapio.query.filter_by(disponivel=True).all()
    
    @staticmethod
    def get_by_categoria(categoria):
        """Buscar itens por categoria"""
        return ItemCardapio.query.filter_by(categoria=categoria, disponivel=True).all()
    
    @staticmethod
    def get_item(item_id):
        """Buscar um item específico"""
        return ItemCardapio.query.get(item_id)
    
    @staticmethod
    def update_item(item_id, nome, descricao, categoria, preco, disponivel):
        """Atualizar um item existente"""
        try:
            item = ItemCardapio.query.get(item_id)
            if not item:
                return False, "Item não encontrado"
            
            item.nome = nome
            item.descricao = descricao
            item.categoria = categoria
            item.preco = preco
            item.disponivel = disponivel
            
            db.session.commit()
            return True, item
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def delete_item(item_id):
        """Deletar um item"""
        try:
            item = ItemCardapio.query.get(item_id)
            if not item:
                return False, "Item não encontrado"
            
            db.session.delete(item)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def __repr__(self):
        return f'<ItemCardapio {self.nome} - R$ {self.preco}>'
