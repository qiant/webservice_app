#!/bin/sh

curl -X POST "http://127.0.0.1:8080/api/uploadResumeDetails" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"John Doe\",\"title\":\"Software Engineer\",\"description\":\"develop software for a fintech firm\",\"company\":\"One Famous Co., LLC\",\"id\":1}"

curl -X POST "http://127.0.0.1:8080/api/uploadResumeDetails" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"Tom Doe\",\"title\":\"Senior Software Engineer\",\"description\":\"develop software in IT firm\",\"company\":\"ACME famous Co.\",\"id\":2}"

curl -X POST "http://127.0.0.1:8080/api/uploadResumeDetails" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"Eric Hanks\",\"title\":\"Software Engineer\",\"description\":\"develop software for a fintech firm\",\"company\":\"ACME famous Co.\"}"

curl -X POST "http://127.0.0.1:8080/api/uploadResumeDetails" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"Eric Smith\",\"title\":\"Software Engineer\",\"description\":\"develop software\",\"company\":\"The Topgun Co., LLC\"}"

curl -X POST "http://127.0.0.1:8080/api/uploadResumeDetails" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\":\"Ron Smith\",\"title\":\"Software Engineer\",\"description\":\"develop software in financial firm\",\"company\":\"ACME Co.\"}"
