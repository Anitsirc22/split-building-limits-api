import json
import logging
import os

import psycopg


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
    INSERT INTO split_building_limits (building_limits, height_plateaus, split_building_limits) VALUES (%s, %s, %s)
"""

SELECT_ROW_QUERY = """
    SELECT (split_building_limits) FROM split_building_limits WHERE building_limits = %s AND height_plateaus = %s
"""

COUNT_ALL_ROWS_QUERY = """
    SELECT COUNT(*) FROM your_table
"""

DELETE_ALL_ROWS_QUERY = """
    DELETE FROM split_building_limits
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
        logger.info("Split building limits written to database.")
    return json.loads(split_building_limits_str)


async def get_existing_split_building_limits(
    async_connection, building_limits_str, height_plateaus_str
):
    """Get split building limits from database."""
    try:
        async with async_connection.cursor() as cursor:
            await cursor.execute(
                SELECT_ROW_QUERY, (building_limits_str, height_plateaus_str)
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
