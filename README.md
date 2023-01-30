# BrightIdeas

users table
| Column | Datatype |
| --- | --- |
| id | INT |
| firstName | VARCHAR(255) |
| lastName | VARCHAR(255) |
| email | VARCHAR(255) |
| password | VARCHAR(255) |
| createdAt | DATETIME |
| updatedAt | DATETIME |


posts table
| Column | Datatype |
| --- | --- |
| id | INT |
| likes | INT |
| content | VARCHAR(255) |
| createdAt | DATETIME |
| updatedAt | DATETIME |
| user_id | INT | 


likes table
| Column | Datatype |
| --- | --- | 
| id | INT |
| user_id | INT |
| post_id | INT |
| createdAt | DATETIME | 
| updatedAt | DATETIME |

