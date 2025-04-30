from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from app.models.primary.parser.BandingDataParser import parse_banding_data

Base = declarative_base()

class AFObject(Base):
    __tablename__ = 'af_object'
    afo_id = Column(Integer, primary_key=True, nullable=False)
    afo_type = Column(Integer, nullable=False)
    afo_h_align = Column(String)
    afo_v_align = Column(String)
    afo_alignment = Column(String)
    afo_bg_colour = Column(String)
    afo_colour_code = Column(String)
    afo_creation_date = Column(DateTime, default=datetime.utcnow)
    afo_description = Column(String)
    afo_domain = Column(String, nullable=False)
    field_label_position = Column(String)
    afo_height = Column(Integer)
    afo_label = Column(String, nullable=False)
    afo_label_align = Column(String)
    afo_label_type = Column(String)
    afo_label_url = Column(String)
    afo_modified_date = Column(DateTime, default=datetime.utcnow)
    afo_name = Column(String, nullable=False)
    afo_unique_string = Column(String, nullable=False)
    afo_width = Column(Integer)
    afo_parent = Column(Integer, ForeignKey('af_object.afo_id'))
    child_index = Column(Integer)
    af_object = relationship('AFObject', remote_side=[afo_id])
    roles = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': -1,
        'polymorphic_on': afo_type
    }

# Child classes

class FormDomain(AFObject):
    __mapper_args__ = {
        'polymorphic_identity': 0
    }

class FormGroup(AFObject):
    __mapper_args__ = {
        'polymorphic_identity': 1
    }

class FormDefinition(AFObject):
    __mapper_args__ = {
        'polymorphic_identity': 2
    }
    formDefinition_allow_notes_attachment = Column(String)
    formDefinition_allow_notification = Column(String)
    formDefinition_Allow_PDF_view = Column(String)
    formDefinition_expression = Column(String)
    formDefinition_liveStatus = Column(Integer)
    formDefinition_notifing_users = Column(String)
    formDefinition_owner = Column(String)
    formDefinition_primaryKeyField = Column(String)
    formDefinition_Publish_To_MobilePortal = Column(String)
    formDefinition_Publish_To_PatientPortal = Column(String)
    formDefinition_show_notes = Column(String)

class FormPage(AFObject):
    __mapper_args__ = {
        'polymorphic_identity': 3
    }
    formPage_sectPerRow = Column(Integer)

class FormSection(AFObject):
    __mapper_args__ = {
        'polymorphic_identity': 4
    }
    columns = Column(Integer)
    show_title = Column(String)

class FormField(AFObject):
    __mapper_args__ = {
        'polymorphic_identity': 5
    }
    formField_AssociatedMedia_Link = Column(String)
    formField_bandingDataXmlValue = Column(String)
    bindExp = Column(String)
    formField_defSequence = Column(String)
    formField_defValMode = Column(Integer)
    formField_defValue = Column(String)
    formField_extRefField = Column(String)
    formField_extRef = Column(String)
    formField_fieldType = Column(Integer)
    formField_filter_childField = Column(Integer)
    formField_filter_HospitalCode = Column(String)
    formField_filter_parentField = Column(Integer)
    formField_input_style = Column(String)
    formField_inputType = Column(Integer)
    formField_max = Column(String)
    formField_mediaTextBlock = Column(String)
    formField_min = Column(String)
    formField_mapDomain = Column(String)
    formField_mapName = Column(String)
    formField_pattern = Column(String)
    formField_referencedField = Column(String)
    formField_required = Column(String)
    formField_style = Column(String)
    formField_syncWithReference = Column(String)

    @property
    def banding_data(self):
        return parse_banding_data(self.formField_bandingDataXmlValue)