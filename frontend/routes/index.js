require("dotenv").config();
var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
const dayjs = require('dayjs');
const utc = require('dayjs/plugin/utc');
dayjs.extend(utc);

let mKey = process.env.MAP_KEY;
// MongoDB Atlas Connection
const MONGO_URI = process.env.MDB_URL;

mongoose.connect(MONGO_URI)
  .then(() => console.log("Connected to MongoDB Atlas"))
  .catch(err => console.error("MongoDB Connection Error:", err));

// Define Tweet Schema
const tweetSchema = new mongoose.Schema({
  user: String,
  text: String,
  query: String,
  timestamp: String,
  latitude: Number,
  longitude: Number,
  disaster_type: String
});

const Tweet = mongoose.model("Tweet", tweetSchema);


// GET home page & Fetch Tweets
router.get('/', async function (req, res, next) {
  try {
    //pull most recent 500 tweets from mongodb to be displayed
    const tweets = await Tweet.find({ disaster_type: { $in: ["tornado", "hurricane", "earthquake", "flood", "wildfire", "blizzard", "haze", "meteor"] } }).sort({ timestamp: -1 }).limit(2000);
    //used by bar graph
    let tCount = await Tweet.find({ disaster_type: { $in: ["tornado"] } }).countDocuments();
    let hCount = await Tweet.find({ disaster_type: { $in: ["hurricane"] } }).countDocuments();
    let eCount = await Tweet.find({ disaster_type: { $in: ["earthquake"] } }).countDocuments();
    let fCount = await Tweet.find({ disaster_type: { $in: ["flood"] } }).countDocuments();
    let wCount = await Tweet.find({ disaster_type: { $in: ["wildfire"] } }).countDocuments();
    let bCount = await Tweet.find({ disaster_type: { $in: ["blizzard"] } }).countDocuments();
    let zCount = await Tweet.find({ disaster_type: { $in: ["haze"] } }).countDocuments();
    let mCount = await Tweet.find({ disaster_type: { $in: ["meteor"] } }).countDocuments();
    let barData = [tCount, hCount, eCount, fCount, wCount, bCount, zCount, mCount];
    console.log(tCount);
    let urlKey=process.env.API_URL;


//calculate date for 2 weeks ago
    const twoWeeksAgo = dayjs.utc().subtract(13, 'day').startOf('day').toDate();
//count number of tweets for specific disaster type per day, starting from two weeks ago onward
    const results = await Tweet.aggregate([
      {
        //compare timestamp to see if its greater than or equal to two weeks ago, and then (UNNECESSARILY SEES IF DISASTER IS IN DISASTERTYPE)
        $match: {
          $expr: {
            $gte: [ { $toDate: "$timestamp" }, twoWeeksAgo ]
          },
          disaster_type: { $in: ["tornado", "hurricane", "earthquake", "flood", "wildfire", "blizzard", "haze", "meteor"] }
        }
      },
      {
        //group docs by day and type, and sum tweets for each group
        $group: {
          _id: {
            day: { $dateToString: { format: "%Y-%m-%d", date: { $toDate: "$timestamp" } } },
            type: "$disaster_type"
          },
          count: { $sum: 1 }
        }
      },
      {
        //sort grouped results by day
        $sort: { "_id.day": 1 }
      }
    ]);

    //generate an array of 14 date strings for the line charts x axis
    const lineLabels = [];
    for (let i = 0; i < 14; i++) {
      lineLabels.push(dayjs().subtract(13 - i, 'day').format('YYYY-MM-DD'));
    }

    const types = ["tornado", "hurricane", "earthquake", "flood", "wildfire", "blizzard", "haze", "meteor"];

    //create obj to hold daily counts for disaster types
    const disasterLineData = {};
    types.forEach(type => {
      disasterLineData[type] = Array(14).fill(0);
    });

    //filling in disasterLineData arrays with counts
    results.forEach(({ _id, count }) => {
      const { day, type } = _id;
      const dayIndex = lineLabels.indexOf(day);
      if (dayIndex !== -1 && disasterLineData[type]) {
        disasterLineData[type][dayIndex] = count;
      }
    });
//send to ejs file
    res.render('index', { title: 'Bluesky Tweets', tweets, mKey, barData, lineLabels, disasterLineData,urlKey });

  } catch (error) {
    res.status(500).send("Error fetching tweets.");
  }
});

module.exports = router;
