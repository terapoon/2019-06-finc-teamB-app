const knex = require('knex');

const client = knex({
  client: 'mysql2',
  connection: {
    host: process.env.DATABASE_HOST || '127.0.0.1',
    user: process.env.DATABASE_USER || 'root',
    password: process.env.DATABASE_PASSWORD || '',
    database: process.env.DATABASE_NAME || 'test',
  },
});

module.exports = client;
