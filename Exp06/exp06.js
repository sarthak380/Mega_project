const express = require('express')
const app = express()
const port = 4000

app.get('/', (req, res) => {
 const time = new Date();

})

app.get('/about', (req, res) => {
    res.send("This is the about page")
})

app.get('/contact', (req, res) => {
    res.send("This is the contact page")
})

 app.use((req, res, next) => {
    console.log("request receive at " + new Date());
    next();
 });
 

app.listen(port, () => {
  console.log(`Example app listening on port https:/localhost/${port}`)
})


// routing : it means decide what respond to send for different URL 
// app.get() : it means when we get a request to the root URL, we will send a response with the current time and a message.
//Middleware : it is a function that returns before sending respose 
 // using this checking data , authenticate user 


 //next()-> use : pass control to the next function .
 // request will hang if we didnt give next()

// two middleware examples 

