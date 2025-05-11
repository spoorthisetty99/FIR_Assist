require('dotenv').config();
const mongoose = require('mongoose');
const Section = require('../models/Section');
const Judgment = require('../models/Judgment');
const connectDB = require('../config/database');

const sections = [
  {
    code: 'IPC 302',
    title: 'Murder',
    description: 'Whoever commits murder shall be punished with death or imprisonment for life',
    keywords: ['murder', 'killing', 'homicide', 'death', 'killed', 'slain']
  },
  {
    code: 'IPC 307',
    title: 'Attempt to Murder',
    description: 'Whoever does any act with such intention or knowledge that if he by that act caused death, he would be guilty of murder',
    keywords: ['attempt', 'murder', 'kill', 'assault', 'tried to kill', 'tried to murder']
  },
  {
    code: 'IPC 376',
    title: 'Rape',
    description: 'Whoever commits rape shall be punished with rigorous imprisonment',
    keywords: ['rape', 'sexual assault', 'molestation', 'raped', 'sexually assaulted']
  },
  {
    code: 'IPC 379',
    title: 'Theft',
    description: 'Whoever commits theft shall be punished with imprisonment',
    keywords: ['theft', 'steal', 'stole', 'robbery', 'larceny', 'stolen', 'robbed', 'snatched']
  },
  {
    code: 'IPC 420',
    title: 'Cheating and Dishonesty',
    description: 'Whoever cheats and thereby dishonestly induces the person deceived to deliver any property',
    keywords: ['cheat', 'fraud', 'deception', 'scam', 'cheated', 'forged', 'forgery', 'fake document']
  },
  {
    code: 'IPC 454',
    title: 'Housebreaking',
    description: 'Lurking house-trespass or house-breaking in order to commit offence punishable with imprisonment',
    keywords: ['housebreaking', 'burglary', 'break-in', 'forcibly entered', 'broke into', 'trespass']
  },
  {
    code: 'IPC 323',
    title: 'Voluntarily Causing Hurt',
    description: 'Whoever voluntarily causes hurt shall be punished',
    keywords: ['hurt', 'injury', 'injuries', 'assault', 'beaten', 'beating', 'attacked']
  }
];

const judgments = [
  {
    caseName: 'State of Maharashtra v. Sukhdev Singh',
    sectionCodes: ['IPC 302'],
    synopsis: 'Landmark case establishing the principles of circumstantial evidence in murder cases',
    date: new Date('1992-05-15'),
    court: 'Supreme Court of India'
  },
  {
    caseName: 'R v. Dudley and Stephens',
    sectionCodes: ['IPC 302'],
    synopsis: 'Famous case dealing with necessity as a defense to murder',
    date: new Date('1884-12-09'),
    court: 'Queen\'s Bench Division'
  },
  {
    caseName: 'State of Punjab v. Gurmit Singh',
    sectionCodes: ['IPC 376'],
    synopsis: 'Important case on rape laws and victim testimony',
    date: new Date('1996-02-13'),
    court: 'Supreme Court of India'
  },
  {
    caseName: 'Kishan Chand v. State of Haryana',
    sectionCodes: ['IPC 379'],
    synopsis: 'Case establishing principles for proving theft and possession of stolen property',
    date: new Date('2013-03-19'),
    court: 'Supreme Court of India'
  }
];

const seedDatabase = async () => {
  try {
    await connectDB();

    // Clear existing data
    await Section.deleteMany({});
    await Judgment.deleteMany({});

    // Insert new data
    await Section.insertMany(sections);
    await Judgment.insertMany(judgments);

    console.log('Database seeded successfully');
    process.exit(0);
  } catch (error) {
    console.error('Error seeding database:', error);
    process.exit(1);
  }
};

seedDatabase(); 