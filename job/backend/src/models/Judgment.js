const mongoose = require('mongoose');

const judgmentSchema = new mongoose.Schema({
  caseName: {
    type: String,
    required: true,
    trim: true
  },
  sectionCodes: [{
    type: String,
    required: true,
    trim: true
  }],
  synopsis: {
    type: String,
    required: true,
    trim: true
  },
  date: {
    type: Date,
    required: true
  },
  court: {
    type: String,
    required: true,
    trim: true
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Judgment', judgmentSchema); 