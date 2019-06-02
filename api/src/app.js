const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const logger = require('./logger');
const routes = require('./routes');

const app = express();
app.use('/uploads', express.static('uploads'));
app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(routes);

app.use((err, req, res, next) => {
  logger.error(err);
  res.sendStatus(500);
});

module.exports = app;
