const express = require('express');
const router = express.Router();
const { analyzeNarrative } = require('../controllers/analyzeController');

router.post('/analyze', analyzeNarrative);

module.exports = router; 