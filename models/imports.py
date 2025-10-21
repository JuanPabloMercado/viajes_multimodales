"""
Centraliza la gestión de los imports para todo el proyecto.
"""

# Python estándar
import re
from datetime import datetime, date, time
from decimal import Decimal, getcontext
getcontext().prec = 10   # cantidad de dígitos significativos
from sqlalchemy.sql import func
from typing import Type
from sqlalchemy import event, select# SQLAlchemy ORM
from sqlalchemy.orm import relationship, validates
# SQLAlchemy Core
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Numeric,
    Boolean,
    Enum,
    ForeignKey,
    Date,
    DateTime,
    func
)
"""
Centraliza la gestión de los imports para todo el proyecto.


# Python estándar
import re
from datetime import datetime, date

# SQLAlchemy Core
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Numeric,
    Boolean,
    Enum,
    ForeignKey,
    Date,
    DateTime,
    func
)

# SQLAlchemy ORM
from sqlalchemy.orm import relationship, validates

# Base de modelos
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
"""






