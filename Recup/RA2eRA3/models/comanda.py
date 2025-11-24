from models.db import db
from datetime import datetime

class Comanda(db.Model):
    __tablename__ = 'comandas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_mesa = db.Column(db.Integer, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='aberta')  # 'aberta', 'fechada', 'paga'
    valor_total = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    fechada_at = db.Column(db.DateTime)
    paga_at = db.Column(db.DateTime)
    
    # Relacionamentos
    cliente = db.relationship('Usuario', back_populates='comandas', foreign_keys=[cliente_id])
    itens = db.relationship('ItemComanda', back_populates='comanda', lazy=True, cascade='all, delete-orphan')
    pagamentos = db.relationship('Pagamento', back_populates='comanda', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, numero_mesa, cliente_id):
        self.numero_mesa = numero_mesa
        self.cliente_id = cliente_id
        self.status = 'aberta'
        self.valor_total = 0.0
    
    @staticmethod
    def save_comanda(numero_mesa, cliente_id):
        """Criar uma nova comanda"""
        try:
            comanda = Comanda(
                numero_mesa=numero_mesa,
                cliente_id=cliente_id
            )
            db.session.add(comanda)
            db.session.commit()
            return True, comanda
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_comandas():
        """Listar todas as comandas"""
        return Comanda.query.order_by(Comanda.created_at.desc()).all()
    
    @staticmethod
    def get_comandas_abertas():
        """Listar comandas abertas"""
        return Comanda.query.filter_by(status='aberta').order_by(Comanda.created_at.desc()).all()
    
    @staticmethod
    def get_comandas_fechadas():
        """Listar comandas fechadas (mas não pagas)"""
        return Comanda.query.filter_by(status='fechada').order_by(Comanda.fechada_at.desc()).all()
    
    @staticmethod
    def get_comandas_pagas():
        """Listar comandas pagas"""
        return Comanda.query.filter_by(status='paga').order_by(Comanda.paga_at.desc()).all()
    
    @staticmethod
    def get_comandas_by_cliente(cliente_id):
        """Listar comandas de um cliente específico"""
        return Comanda.query.filter_by(cliente_id=cliente_id).order_by(Comanda.created_at.desc()).all()
    
    @staticmethod
    def get_comanda(comanda_id):
        """Buscar uma comanda específica"""
        return Comanda.query.get(comanda_id)
    
    def calcular_total(self):
        """Calcular o valor total da comanda"""
        total = sum(item.subtotal for item in self.itens)
        self.valor_total = total
        db.session.commit()
        return total
    
    def fechar_comanda(self):
        """Fechar a comanda (não permite mais adicionar itens)"""
        try:
            if self.status != 'aberta':
                return False, "Comanda já está fechada ou paga"
            
            self.calcular_total()
            self.status = 'fechada'
            self.fechada_at = datetime.now()
            db.session.commit()
            return True, self
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def reabrir_comanda(self):
        """Reabrir uma comanda fechada (apenas caixa pode fazer isso)"""
        try:
            if self.status == 'paga':
                return False, "Comanda já foi paga, não pode ser reaberta"
            
            self.status = 'aberta'
            self.fechada_at = None
            db.session.commit()
            return True, self
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def marcar_como_paga(self):
        """Marcar comanda como paga (apenas caixa pode fazer isso)"""
        try:
            if self.status == 'aberta':
                return False, "Comanda precisa estar fechada antes de ser paga"
            
            if self.status == 'paga':
                return False, "Comanda já está paga"
            
            self.status = 'paga'
            self.paga_at = datetime.now()
            db.session.commit()
            return True, self
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def __repr__(self):
        return f'<Comanda #{self.id} - Mesa {self.numero_mesa} - {self.status}>'
