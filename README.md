# Description
Quranic sound recognizer to detect any wrong recitation using Deep Learning technique

# Telegram Bot
Available on telegram with username @the_recitation_bot
Link: https://telegram.me/@the_recitation_bot

# Technology Spec
* Database: Mongo
* Algorithm: Convolutional Neural Network
* Containerization: Docker CE
* Orchestration: Docker Swarm

# DB Design
It's json structured contains 2 schema

### user
* telegram_id
* username
* current_verse
* current_ayah
* stage_level
* score

### stage_available
* stage_number
* verse_number
* total_ayah

# References
*
*
