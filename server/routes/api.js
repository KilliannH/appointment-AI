const router = require('express').Router();
var moment = require('moment');
var momentTZ = require('moment-timezone');
momentTZ().tz("Europe/Berlin").format();

var Sequelize = require('sequelize');
const config = require('../config/database');

//Connect to Postgre
const sequelize = new Sequelize(config.postgresPath);

//Db connection
sequelize
    .authenticate()
    .then(() => {
        console.log('Db connected...');
    })
    .catch(err => {
        console.error('Unable to connect to the database:', err);
    });

//init appointment model
const Appointment = sequelize.define('Appointments', {

    name: {
        type: Sequelize.STRING
    },
    date: {
        type: Sequelize.BIGINT
    },
    created_date: {
        type: Sequelize.BIGINT
    },
    sent: {
        type: Sequelize.BOOLEAN
    },
    voice_alerted: {
        type: Sequelize.BOOLEAN
    }
}, {timestamps: false});


// DEFAULT GET HERE ///
router.get('/appointments', function (req, res) {

    Appointment.findAll().then(appointments => appointments ? res.json(appointments) : res.json({succes: false, message: "Failed to get appointments"}));
});

/// GET Appointement BY id ///
router.get('/appointments/id=:id', function (req, res) {

    Appointment.find({
        where: {
            id: req.params.id
        }
    }).then((appointment) => appointment ? res.json(appointment) : res.json({success: false, message: 'an errorr occured, appointment might not exist'}))
});

/// GET Appointement BY name ///
router.get('/appointments/name=:name', function (req, res) {

    Appointment.find({
        where: {
            name: req.params.name
        }
    }).then((appointment) => appointment ? res.json(appointment) : res.json({success: false, message: 'an errorr occured, appointment might not exist'}))
});

/// GET Appointements BY periods ///
router.get('/appointments/period=:period', function (req, res) {
    console.log(`${req.params.period} detected`);

    let periods = ["today", "tomorrow",
        "thisWeek", "nextWeek", "thisMonth"];

    //Tools
    let today = Date.now();
    let tomorrow = moment(today).add(1, 'd').endOf('day');
    let nextSunday;
    if(moment(today).get('day') !== 6) {
        nextSunday = moment().day("Saturday").add(1, 'd').endOf('day');
    } else {
        nextSunday = moment().add(8, 'd').endOf('day');
        console.log(nextSunday);

    }
    //console.log(nextSunday);
    let endOfMonth = moment().endOf('month');

    let output = [];

    return Appointment.findAll().then(appointments => {

        // today
        if(req.params.period === periods[0]) {
            for(let i = 0; i < appointments.length; i++) {
                let appointmentDate = new Date(appointments[i].date * 1000);
                if(moment(today).isSame(moment(appointmentDate), 'day')) {
                    output.push(appointments[i]);
                }
            }
            return res.json(output)

            // tomorrow
        } else if(req.params.period === periods[1]) {
            for(let i = 0; i < appointments.length; i++) {
                let appointmentDate = new Date(appointments[i].date * 1000);
                if(moment(appointmentDate).isSameOrAfter(moment(today)) && moment(appointmentDate).isSameOrBefore(moment(tomorrow))) {
                    output.push(appointments[i]);
                }
            }
            console.log(output.length);
            return res.json(output)

            // next week
        } else if(req.params.period === periods[2] || req.params.period === periods[3]) {
            for(let i = 0; i < appointments.length; i++) {
                let appointmentDate = new Date(appointments[i].date * 1000);
                if(moment(appointmentDate).isSameOrAfter(moment(today)) && moment(appointmentDate).isSameOrBefore(moment(nextSunday))) {
                    output.push(appointments[i]);
                }
            }
            return res.json(output)

            // next month
        } else if(req.params.period === periods[4]) {
            for(let i = 0; i < appointments.length; i++) {
                let appointmentDate = new Date(appointments[i].date * 1000);
                if(moment(appointmentDate).isSameOrAfter(moment(today)) && moment(appointmentDate).isSameOrBefore(moment(endOfMonth))) {
                    output.push(appointments[i]);
                }
            }
            return res.json(output)
        }
    }).catch(e => res.json({success: false, message: e}));
});

/// POST NEW Appointment ///
router.post('/appointments', (req, res) => {

    let createdDate = Date.now()
    createdDate = parseInt(createdDate / 1000);

    Appointment.create({
        name: req.body.name,
        date: req.body.date,
        created_date: createdDate,
        sent: false,
        voice_alerted: false
    }).then((appointment) => appointment ? res.json(appointment) : res.json({success: false, message: "failed to post appointment"}))
});

/// PUT Appointment ///
router.put('/appointments/:id', (req, res) => {
    Appointment.find({
        where: {
            id: req.params.id
        }
    }).then((appointment) => appointment.updateAttributes({
        name: req.body.name,
        date: req.body.date,
        sent: req.body.sent,
        vocal_alerted: req.body.vocal_alerted
    }).then((appointmentUpdated) => appointmentUpdated ? res.json(appointmentUpdated) : res.json({success: false, message: 'failed to update appointment, please try again'})))
});

/// DELETE appointment ///
router.delete('/appointments/id=:id', function (req, res) {

    Appointment.destroy({
        where: {
            id: req.params.id
        }
    }).then((appointment) => appointment ? res.json(appointment.id) : res.json({success: false, message: 'an error occured, this appointment may not exist'}))
});

module.exports = router;