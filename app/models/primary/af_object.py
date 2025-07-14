"""
Module defining the AFObject model hierarchy for form-related entities.

This module provides a polymorphic ORM model representing form objects,
including domains, groups, definitions, pages, sections, and fields.
Each subclass specializes attributes relevant to its role in form management.

The AFObject base model supports parent-child relationships and common
attributes such as alignment, colors, dimensions, and roles.

The FormField subclass includes a property to parse embedded banding data XML.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.config import Base
from app.models.primary.parser.banding_data_parser import parse_banding_data


class AFObject(Base):
    """
    Serves as the base model for form objects, providing common attributes and polymorphic behavior for various form-related entities.
    Attributes:
    afo_id : int
        Unique identifier for the form object.
    afo_type : int
        Type identifier for polymorphic differentiation.
    afo_h_align : str
        Horizontal alignment setting.
    afo_v_align : str
        Vertical alignment setting.
    afo_alignment : str
        General alignment configuration.
    afo_bg_colour : str
        Background color of the object.
    afo_colour_code : str
        Color code for additional customization.
    afo_creation_date : datetime
        Date and time of creation.
    afo_description : str
        Description of the form object.
    afo_domain : str
        Domain context of the form object.
    field_label_position : str
        Position of the field label.
    afo_height : int
        Height dimension of the object.
    afo_label : str
        Label associated with the form object.
    afo_label_align : str
        Alignment for the label.
    afo_label_type : str
        Type of the label.
    afo_label_url : str
        URL associated with the label.
    afo_modified_date : datetime
        Date and time of the last modification.
    afo_name : str
        Name of the form object.
    afo_unique_string : str
        Unique string identifier.
    afo_width : int
        Width dimension of the object.
    afo_parent : int
        Reference to a parent object.
    child_index : int
        Index to differentiate children in a parent-child structure.
    roles : str
        Roles associated with the object.

    Relationships:
    af_object : relationship Self-referential relationship for parent-child hierarchy.

    Polymorphism:
    This model uses polymorphic inheritance to define specific subtypes of form objects.
    """
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
    """
    Represents a domain within which forms operate, inheriting common attributes from AFObject.
    """
    __mapper_args__ = {
        'polymorphic_identity': 0
    }

class FormGroup(AFObject):
    """ Represents a group of forms, inheriting from AFObject. """
    __mapper_args__ = {
        'polymorphic_identity': 1
    }

class FormDefinition(AFObject):
    """
      Provides detailed definitions for forms,
      extending AFObject with specific attributes for form configuration.
      Attributes:
      formDefinition_allow_notes_attachment : str
          Flag for allowing notes attachments.
      formDefinition_allow_notification : str
          Flag for enabling notifications.
      formDefinition_Allow_PDF_view : str
          Flag for PDF view permissions.
      formDefinition_expression : str
          Expression for form logic.
      formDefinition_liveStatus : int
          Status indicating if the form is live.
      formDefinition_notifing_users : str
          Users to notify about form events.
      formDefinition_owner : str
          Owner of the form.
      formDefinition_primaryKeyField : str
          Primary key field for the form.
      formDefinition_Publish_To_MobilePortal : str
          Flag for mobile portal publication.
      formDefinition_Publish_To_PatientPortal : str
          Flag for patient portal publication.
      formDefinition_show_notes : str Flag for displaying notes."""
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
    """
     Represents a page within a form, inheriting from AFObject.
      This model is designed to manage the layout and content organization within a form,
      ensuring a structured presentation of form elements.
    Attributes:
    formPage_sectPerRow : int Number of sections displayed per row on the form page.
    """
    __mapper_args__ = {
        'polymorphic_identity': 3
    }
    formPage_sectPerRow = Column(Integer)

class FormSection(AFObject):
    """
     Represents a section within a form page, inheriting from AFObject.
     This model is used to organize form fields into logical groups,
      enhancing the readability and usability of forms.
    Attributes:
    columns : int Number of columns in the section, determining the layout structure.
    show_title : str  Flag indicating whether to display the section title.
    """
    __mapper_args__ = {
        'polymorphic_identity': 4
    }
    columns = Column(Integer)
    show_title = Column(String)

class FormField(AFObject):
    """
    Represents an individual field within a form section, inheriting from AFObject.
    This model is crucial for capturing user input and managing the display and behavior of form fields.
    Attributes:
    formField_AssociatedMedia_Link : str Link to media associated with the form field.
    formField_bandingDataXmlValue : str XML data for banding information.
    bindExp : str Binding expression for dynamic data associations.
    formField_defSequence : str Sequence definition for form field ordering.
    formField_defValMode : int  Default value mode indicating how values are determined.
    formField_defValue : str  Default value for the form field.
    formField_extRefField : str External reference field.
    formField_extRef : str External reference for extended data linking.
    formField_fieldType : int  Type indicator for the form field.
    formField_filter_childField : int Filter criteria for child fields.
    formField_filter_HospitalCode : str  Filter criteria based on hospital code.
    formField_filter_parentField : int  Filter criteria for parent fields.
    formField_input_style : str Style attributes for the field input.
    formField_inputType : int Input type (e.g., text, number).
    formField_max : str Maximum value constraint.
    formField_mediaTextBlock : str Text block for media content.
    formField_min : str Minimum value constraint.
    formField_mapDomain : str Domain mapping for the field.
    formField_mapName : strMapping name for data associations.
    formField_pattern : str Pattern for validating input.
    formField_referencedField : str Field referenced for additional data.
    formField_required : str Flag indicating if the field is mandatory.
    formField_style : str Style attributes for the field.
    formField_syncWithReference : str Flag for syncing with reference data.
    Properties:
    banding_data : property Parses and returns banding data from the XML string.
    """
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
