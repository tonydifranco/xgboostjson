const http = require('http');
const url = require('url');
const fs = require('fs');
const spawn = require('child_process').spawn;
const model = require('./R/model.js');
// or
// const model = require('./python/model.js');
http.createServer(function(request, response){
	let q = url.parse(request.url, true).query;
	if(Object.keys(q) == 0){
		fs.readFile('./demo.html', function(error, data){
			response.end(data, 'utf-8');
		});
	}else{
		let method = q.method;
		delete q.method;
		if(method == 'node'){
			response.end(model.predict(q).toFixed(3), 'utf-8');
		}else if(method == 'r'){
			let RCall = ['--vanilla', 'R/child_process.R', JSON.stringify(q)];
			let R = spawn("Rscript", RCall, {cwd: '.', env: process.env})
			R.stdout.on("data", function(data){
				response.end(data, 'utf-8');
			});
		}else if(method == 'python'){
			let pyCall = ['python/child_process.py', JSON.stringify(q)];
			let python = spawn("python", pyCall, {cwd: '.', env: process.env})
			python.stdout.on("data", function(data){
				response.end(data, 'utf-8');
			});
		}else{
			resonse.writeHead(500).end('error!');
		}
	}
}).listen(8080);