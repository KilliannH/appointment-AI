const api = require('./routes/api');
//Server imports
const express = require('express');
const bodyParser = require('body-parser');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

/// DEFAULT GET HERE ///
app.get('/', function (req, res) {
    res.send('Please use /api/appointments');
});

app.use('/api', api);
let port = 3000;

app.listen(port);
console.log(`App running on port ${port}`);