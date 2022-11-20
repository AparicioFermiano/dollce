# def connect(self):
#     host, _, port = self.config.postgresql_host.partition(':')

#     ssl_kwargs = {}
#     if self.config.postgresql_ssl_enabled:
#         ssl_kwargs['sslmode'] = 'verify-full'
#         ssl_kwargs['sslrootcert'] = self.config.postgresql_ca_cert_path

#         # It only makes sense to check this if SSL is on
#         if self.config.postgresql_ssl_client_verification:
#             ssl_kwargs['sslcert'] = self.config.postgresql_ssl_cert_path
#             ssl_kwargs['sslkey'] = self.config.postgresql_ssl_key_path

#     return psycopg2.connect(
#         dbname=self.config.postgresql_db_name,
#         host=host,
#         port=port or 5432,
#         user=self.config.postgresql_username,
#         password=self.config.postgresql_password,
#         cursor_factory=DictCursor,
#         **ssl_kwargs
#     )