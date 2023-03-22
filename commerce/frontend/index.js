
fetch('http://localhost:8000/api/listings/')
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.log(err))