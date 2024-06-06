"""Module containing models for process outputs"""

# pylint: disable=no-name-in-module

from langchain_core.pydantic_v1 import BaseModel, Field


class ProcessA1(BaseModel):
    """
    Model for output of process A1
    """

    ad_description: str = Field(description="description of the advert")
    ad_purpose: str = Field(
        description="can only be either 'brand-building' or 'conversion'"
    )


class ProcessA2(BaseModel):
    """
    Model for output of process A2
    """

    saliency_description: str = Field(
        description="description of the visually salient elements in the advertisement"
    )


class ProcessB(BaseModel):
    """
    Model for output of process B
    """

    cognitive_description: str = Field(
        description="assessment of the cognitive load induced by the advertisement in viewers"
    )


class ProcessC(BaseModel):
    """
    Model for output of process C
    """

    ad_description: str = Field(
        description="summarised versions of the text provided as input"
    )
    ad_purpose: str = Field(
        description="summarised versions of the text provided as input"
    )
    saliency_description: str = Field(
        description="summarised versions of the text provided as input"
    )
    cognitive_description: str = Field(
        description="summarised versions of the text provided as input"
    )
