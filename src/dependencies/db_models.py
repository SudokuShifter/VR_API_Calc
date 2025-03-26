from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
    ARRAY
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class VRZifObjects(Base):
    __tablename__ = 'vr_zif_objects'
    __table_args__ = {'schema': 'vr_scheme'}

    id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
    name = Column(
        String(255)
    )
    hole_project_id = Column(
        Integer, nullable=False
    )
    active_adaptation_value_id = Column(
        BigInteger, default=0
    )
    creation_date = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    active_vr_type = Column(
        String(255), ForeignKey('vr_scheme.vr_type.id')
    )
    current_date_scheduler = Column(
        DateTime
    )
    scheduler_status = Column(
        String(255), ForeignKey('vr_scheme.vr_scheduler_status.id')
    )


    adaptation_data = relationship(
        "VRAdaptationData", back_populates="vr_zif_object"
    )
    validation_data = relationship(
        "VRValidationData", back_populates="vr_zif_object"
    )
    additional_objects = relationship(
        "VRZifAdditionalObjects",
        secondary="vr_scheme.vr_zif_object_2_additional_object",
        back_populates="zif_objects"
    )


class VRAdaptationData(Base):
    __tablename__ = 'vr_adaptation_data'
    __table_args__ = {'schema': 'vr_scheme'}

    id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
    vr_zif_objects_id = Column(
        BigInteger, ForeignKey('vr_scheme.vr_zif_objects.id'), nullable=False
    )
    name = Column(
        String(255)
    )
    choke_percent_adapt = Column(
        ARRAY(Float), nullable=False
    )
    choke_value_adapt = Column(
        ARRAY(Float), nullable=False
    )
    date_start = Column(
        DateTime, nullable=False
    )
    date_end = Column(
        DateTime, nullable=False
    )
    creation_date = Column(
        DateTime, nullable=False
    )


    vr_zif_object = relationship(
        "VRZifObjects", back_populates="adaptation_data"
    )


class VRZifAdditionalObjects(Base):
    __tablename__ = 'vr_zif_additional_objects'
    __table_args__ = {'schema': 'vr_scheme'}

    id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
    name = Column(
        String(255)
    )
    creation_date = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )


    zif_objects = relationship(
        "VRZifObjects",
        secondary="vr_scheme.vr_zif_object_2_additional_object",
        back_populates="additional_objects"
    )


class VRValidationData(Base):
    __tablename__ = 'vr_validation_data'
    __table_args__ = {'schema': 'vr_scheme'}

    id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
    vr_zif_objects_id = Column(
        BigInteger, ForeignKey('vr_scheme.vr_zif_objects.id'), nullable=False
    )
    wct = Column(
        Float, nullable=False
    )
    gas_condensate_factor = Column(
        Float, nullable=False
    )
    is_user_value = Column(
        Boolean, nullable=False
    )
    date = Column(
        DateTime, nullable=False
    )


    vr_zif_object = relationship(
        "VRZifObjects", back_populates="validation_data"
    )


class VRZifObject2AdditionalObject(Base):
    """
    ManyToMany таблица, связывающая vr_zif_additional_objects и vr_zif_object
    """
    __tablename__ = 'vr_zif_object_2_additional_object'
    __table_args__ = {'schema': 'vr_scheme'}

    id = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
    vr_zif_objects_id = Column(
        BigInteger, ForeignKey('vr_scheme.vr_zif_objects.id'), nullable=False
    )
    vr_zif_additional_objects_id = Column(
        BigInteger, ForeignKey('vr_scheme.vr_zif_additional_objects.id'), nullable=False
    )
    name_train = Column(
        String(255)
    )


class VRType(Base):
    __tablename__ = 'vr_type'
    __table_args__ = {'schema': 'vr_scheme'}

    id = Column(
        String(255), primary_key=True
    )
    description = Column(
        String(255)
    )


class VRSchedulerStatus(Base):
    __tablename__ = 'vr_scheduler_status'
    __table_args__ = {'schema': 'vr_scheme'}

    id = Column(
        String(255), primary_key=True
    )
    description = Column(
        String(255)
    )