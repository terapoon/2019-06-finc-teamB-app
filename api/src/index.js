const app = require('./app');
const logger = require('./logger');

const port = process.env.PORT || 4000;

app.listen(port, () => {
  logger.log(`listening on ${port}`);
});
