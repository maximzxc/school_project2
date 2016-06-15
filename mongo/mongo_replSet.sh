sudo docker network create --subnet=10.11.0.0/16 mongo_repl_net

sudo docker run --net mongo_repl_net --ip 10.11.0.11 --name mongo1 -p 27017:27017 -d mongo --enableMajorityReadConcern --replSet rs0 --smallfiles --oplogSize 128
sudo docker run --net mongo_repl_net --ip 10.11.0.12 --name mongo2 -p 27018:27017 -d mongo --enableMajorityReadConcern --replSet rs0 --smallfiles --oplogSize 128
sudo docker run --net mongo_repl_net --ip 10.11.0.13 --name mongo3 -p 27019:27017 -d mongo --enableMajorityReadConcern --replSet rs0 --smallfiles --oplogSize 128

mongo --host 10.11.0.11

rsconf = { 
_id: "rs0", 
members: [ 
	{ _id: 0, host: "10.11.0.11" }, 
	{ _id: 1, host: "10.11.0.12" }, 
	{ _id: 2, host: "10.11.0.13", priority: 0 }
	]
}

rs.initiate( rsconf )
