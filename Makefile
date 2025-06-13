build: 
	docker build -t demianight/anti_spam_deleter:latest .
run:
	docker run --name anti_spam_deleter -e KAFKA_BROKER=62.113.119.235:30092 demianight/anti_spam_deleter
kill:
	docker rm -f anti_spam_deleter
push:
	docker push demianight/anti_spam_deleter:latest
prod:
	docker buildx build --platform linux/amd64 -t demianight/anti_spam_deleter:latest --push .
