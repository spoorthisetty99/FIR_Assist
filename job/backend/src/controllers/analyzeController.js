const Section = require('../models/Section');
const Judgment = require('../models/Judgment');
const natural = require('natural');

const tokenizer = new natural.WordTokenizer();
const stemmer = natural.PorterStemmer;

// Enhanced keyword-based matching with stemming and phrase matching
const getSectionScores = async (narrative, tokens, stemmedTokens) => {
  const sections = await Section.find({});
  const lowerNarrative = narrative.toLowerCase();
  const scores = sections.map(section => {
    let score = 0;
    section.keywords.forEach(keyword => {
      const lowerKeyword = keyword.toLowerCase();
      // Phrase match
      if (lowerKeyword.includes(' ')) {
        if (lowerNarrative.includes(lowerKeyword)) {
          score += 2; // Give higher weight to phrase match
        }
      } else {
        // Stem match
        if (stemmedTokens.includes(stemmer.stem(lowerKeyword))) {
          score += 1;
        }
      }
    });
    return { section, score };
  });
  // Sort by score descending and take top 5
  return scores.filter(s => s.score > 0).sort((a, b) => b.score - a.score).slice(0, 5);
};

const analyzeNarrative = async (req, res) => {
  try {
    const { narrative } = req.body;

    if (!narrative) {
      return res.status(400).json({
        success: false,
        error: 'Please provide a narrative'
      });
    }

    // Preprocess the narrative
    const tokens = tokenizer.tokenize(narrative.toLowerCase());
    const stemmedTokens = tokens.map(token => stemmer.stem(token));

    // Get section scores based on enhanced matching
    const topSections = await getSectionScores(narrative, tokens, stemmedTokens);

    // Fetch section details and related judgments
    const recommendations = await Promise.all(
      topSections.map(async ({ section, score }) => {
        const judgments = await Judgment.find({
          sectionCodes: section.code
        }).limit(2);

        return {
          code: section.code,
          title: section.title,
          description: section.description,
          score: Math.min(score / section.keywords.length, 1),
          judgments: judgments.map(j => ({
            caseName: j.caseName,
            synopsis: j.synopsis
          }))
        };
      })
    );

    res.json({
      success: true,
      recommendations
    });

  } catch (error) {
    console.error('Analysis error:', error);
    res.status(500).json({
      success: false,
      error: 'Error analyzing narrative'
    });
  }
};

module.exports = {
  analyzeNarrative
}; 