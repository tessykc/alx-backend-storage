-- SQL script that creates a stored procedure ComputeAverageScoreForUser 
-- that computes and store the average score for a student. 
-- Note: An average score can be a decimal
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;

    -- Compute the total score for the user
    SELECT SUM(score) INTO total_score
    FROM corrections
    WHERE user_id = user_id;

    -- Compute the total number of projects
    SELECT COUNT(DISTINCT project_id) INTO total_projects
    FROM corrections
    WHERE user_id = user_id;

    -- Calculate the average score (rounded to 2 decimal places)
    SET @average_score := ROUND(total_score / total_projects, 2);

    -- Update the user's average score
    UPDATE users
    SET average_score = @average_score
    WHERE id = user_id;
END;

$$
DELIMITER ;
