from typing import Literal

import geopandas as gpd

from pydantic import BaseModel, Extra, StrictInt, confloat, validator

from src.exceptions import InputGeometryError, InputValueError


StrictFloat = confloat(strict=True, gt=float("-inf"), lt=float("inf"))


class GeometryModel(BaseModel):
    type: str
    coordinates: list[list[list[StrictFloat | StrictInt]]]

    @validator("coordinates")
    def check_coordinates(cls, coordinates):
        """Validate coordinates.

        - Polygons do not contain donut holes (inner rings)
        - Each coordinate pair contains exactly 2 or 3 floats: 3d coordinates can be provided in the input geojson but operations are only performed on 2D geometric data

        """
        if len(coordinates) != 1:
            # For type "Polygon", the "coordinates" member must be an array of LinearRing coordinate arrays. For Polygons with multiple rings, the first must be the exterior ring and any others must be interior rings or holes.
            # https://rdrr.io/cran/geoops/man/Polygon.html
            raise InputGeometryError("Polygons cannot contain inner holes.")
        for coord in coordinates[0]:
            if (num_coord := len(coord)) not in [
                2,
                3,
            ]:
                raise InputGeometryError(
                    f"Coordinates provided contain {num_coord} dimensions. Only 2d or 3d geometries supported."
                )
        return coordinates


class FeatureModel(BaseModel):
    type: Literal["Feature"]
    geometry: GeometryModel
    properties: dict

    class Config:
        extra = Extra.ignore  # ignore extra geojson fields (e.g. bbox, id)


class FeatureCollectionModel(BaseModel):
    type: Literal["FeatureCollection"]
    features: list[FeatureModel]

    class Config:
        extra = Extra.ignore  # ignore extra geojson fields (e.g. bbox)


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

    @validator("height_plateaus")
    def check_split_building_limits(cls, height_plateaus):
        """Validate that height plateaus contain elevation information."""
        for feature in height_plateaus.features:
            if not feature.properties:
                raise InputValueError(
                    "Height plateaus should contain elevation information."
                )
        return height_plateaus


class OutputModel(BaseModel):
    id: int
    split_building_limits: FeatureCollectionModel

    @validator("split_building_limits")
    def check_split_building_limits(cls, split_building_limits):
        """Validate that split building limits contain elevation information."""
        for feature in split_building_limits.features:
            if not feature.properties:
                raise ValueError(
                    "The split building limits should contain elevation information."
                )
        return split_building_limits


class ErrorMessageModel(BaseModel):
    message: str
