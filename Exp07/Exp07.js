const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('Hello World!')
})


app.get('/users/:id', (req, res) => {
    const users = [
        { id: 1, name: 'Yash', age: 21 },
        { id: 2, name: 'ganesh', age: 30 },
        { id: 3, name: 'pradip', age: 35 }
    ];

    const id = parseInt(req.params.id, 10);
    const user = users.find(u => u.id === id);

    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }

    res.json(user);
});





app.listen(port, () => {
  console.log(`Example app listening on port http://localhost/${port}`)
})



