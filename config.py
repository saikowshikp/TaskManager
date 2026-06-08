class Config:
    SECRET_KEY = "SECRET_KEY"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost:3306/taskdb"
    SQLALCHEMY_ECHO = True
    JWT_SECRET_KEY = "083571a4f12f3084616080ec"