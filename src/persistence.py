import logging
import os

import psycopg

from src.exceptions import SplitBuildingLimitsNotFoundError


logger = logging.getLogger(__name__)

# SQL statements
CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS split_building_limits (
        id SERIAL PRIMARY KEY,
        building_limits JSONB,
        height_plateaus JSONB,
        split_building_limits JSONB
    )
"""

INSERT_ROW_QUERY = """
    INSERT INTO split_building_limits (building_limits, height_plateaus, split_building_limits) VALUES (%s, %s, %s) RETURNING id
"""

SELECT_ROW_QUERY_BY_GEOMETRY = """
    SELECT (id, split_building_limits) FROM split_building_limits WHERE building_limits = %s AND height_plateaus = %s
"""

SELECT_ROW_BY_ID_QUERY = """
    SELECT (id, split_building_limits) FROM split_building_limits WHERE id = %s
"""

COUNT_ALL_ROWS_QUERY = """
    SELECT COUNT(*) FROM split_building_limits
"""

DELETE_ALL_ROWS_QUERY = """
    DELETE FROM split_building_limits
"""

DELETE_BY_ID_QUERY = """
    DELETE FROM split_building_limits WHERE id = %s
"""

url = os.environ.get("DB_URL")


async def get_connection():
    """Create a connection to the database."""
    return await psycopg.AsyncConnection.connect(url)


async def write_split_building_limits_to_database(
    async_connection,
    building_limits_str,
    height_plateaus_str,
    split_building_limits_str,
):
    """Write split building limits to database."""
    async with async_connection.cursor() as cursor:
        await cursor.execute(CREATE_TABLE_QUERY)
        await cursor.execute(
            INSERT_ROW_QUERY,
            (building_limits_str, height_plateaus_str, split_building_limits_str),
        )
        row_id = await cursor.fetchone()

        logger.info(
            f"Split building limits written to database, row id is {row_id[0]}."
        )
    # return json.loads(split_building_limits_str)
    return row_id[0]


async def get_existing_split_building_limits(
    async_connection, building_limits_str, height_plateaus_str
) -> tuple | None:
    """Get split building limits from database."""
    try:
        async with async_connection.cursor() as cursor:
            await cursor.execute(
                SELECT_ROW_QUERY_BY_GEOMETRY, (building_limits_str, height_plateaus_str)
            )
            row = await cursor.fetchone()
            logger.info("Split building limits retrieved from database.")
        return row[0] if row else None
    except psycopg.errors.UndefinedTable:
        logging.info("Table does not exist.")
        return None


async def get_number_of_rows():
    """Get number of rows in database."""
    async with await psycopg.AsyncConnection.connect(url) as async_connection:
        async with async_connection.cursor() as cursor:
            await cursor.execute(COUNT_ALL_ROWS_QUERY)
            row = await cursor.fetchone()
            logger.info("Number of rows in database retrieved.")
    return row[0] if row else 0


# elephantsql: SELECT height_plateaus ->> 'features' AS height_plateaus FROM split_building_limits


async def delete_all_rows():
    """Delete all rows from the table."""
    async with await psycopg.AsyncConnection.connect(url) as async_connection:
        async with async_connection.cursor() as cursor:
            await cursor.execute(DELETE_ALL_ROWS_QUERY)
            return {"message": "All rows deleted from the database."}


async def delete_by_id(id: int):
    """Delete a row by id from the data base."""
    async with await psycopg.AsyncConnection.connect(url) as async_connection:
        async with async_connection.cursor() as cursor:
            await cursor.execute(
                SELECT_ROW_BY_ID_QUERY, (id,)
            )  # check if the row exists
            row = await cursor.fetchone()
            if row:
                await cursor.execute(DELETE_BY_ID_QUERY, (id,))
                logger.info(f"Row with id {id} deleted from the database.")
                return {"message": f"Row with id {id} deleted from the database."}
            else:
                raise SplitBuildingLimitsNotFoundError(
                    f"Split building limits with id {id} not found."
                )


async def get_by_id(id: int) -> tuple | None:
    """Delete a row by id from the data base."""
    async with await psycopg.AsyncConnection.connect(url) as async_connection:
        async with async_connection.cursor() as cursor:
            await cursor.execute(SELECT_ROW_BY_ID_QUERY, (id,))
            row = await cursor.fetchone()
            if row:
                logger.info(f"Get by id: {id}.")
                return row[0]
            else:
                raise SplitBuildingLimitsNotFoundError(
                    f"Split building limits with id {id} not found."
                )
