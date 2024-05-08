 --SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
--that computes and store the average weighted score for a student.
--Procedure ComputeAverageScoreForUser is taking 1 input:
--user_id, a users.id value (you can assume user_id is linked to an existing users)
--Calculate-Weighted-Average
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weights INT;

    -- Compute the total weighted score for the user
    SELECT SUM(score * weight) INTO total_weighted_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Compute the total weights
    SELECT SUM(weight) INTO total_weights
    FROM projects;

    -- Calculate the average weighted score (rounded to 2 decimal places)
    SET @average_weighted_score := ROUND(total_weighted_score / total_weights, 2);

    -- Update the user's average score
    UPDATE users
    SET average_score = @average_weighted_score
    WHERE id = user_id;
END;

$$
DELIMITER ;
