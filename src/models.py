from typing import Literal

import geopandas as gpd

from pydantic import BaseModel, Extra, StrictInt, confloat, validator


StrictFloat = confloat(strict=True, gt=float("-inf"), lt=float("inf"))


class GeometryModel(BaseModel):
    type: str
    coordinates: list[list[list[StrictFloat | StrictInt]]]

    @validator("coordinates")
    def check_coordinates(cls, coordinates):
        """Validate coordinates.

        - Polygons do not contain donut holes (inner rings)
        - Each coordinate pair contains exactly 2 floats

        """
        # For type "Polygon", the "coordinates" member must be an array of LinearRing coordinate arrays. For Polygons with multiple rings, the first must be the exterior ring and any others must be interior rings or holes.
        # https://rdrr.io/cran/geoops/man/Polygon.html
        if len(coordinates) != 1:
            raise ValueError("Polygons can not contain donut holes.")
        for coord in coordinates[0]:
            if len(coord) != 2:
                raise ValueError(
                    "Each coordinate pair should contain exactly 2 floats."
                )
        return coordinates


class FeatureModel(BaseModel):
    type: Literal["Feature"]
    geometry: GeometryModel
    properties: dict

    class Config:
        extra = Extra.ignore  # ignore id, bbox


class FeatureCollectionModel(BaseModel):
    type: Literal["FeatureCollection"]
    features: list[FeatureModel]

    class Config:
        extra = Extra.ignore  # ignore bbox


class InputModel(BaseModel):
    building_limits: FeatureCollectionModel
    height_plateaus: FeatureCollectionModel

    def to_geodataframes(self, gcs):
        building_limits_gdf = gpd.GeoDataFrame.from_features(
            self.building_limits.dict(), crs=gcs
        )
        height_plateaus_gdf = gpd.GeoDataFrame.from_features(
            self.height_plateaus.dict(), crs=gcs
        )
        return building_limits_gdf, height_plateaus_gdf


class OutputModel(BaseModel):
    building_limits: FeatureCollectionModel
    height_plateaus: FeatureCollectionModel
    split_building_limits: FeatureCollectionModel

    @validator("split_building_limits")
    def check_split_building_limits(cls, split_building_limits):
        """Validate that the split building limits contain elevation information."""
        for feature in split_building_limits.features:
            if not feature.properties:
                raise ValueError(
                    "The split building limits should contain elevation information."
                )
        return split_building_limits
