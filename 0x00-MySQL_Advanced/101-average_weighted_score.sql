--SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
--that computes and store the average weighted score for all students.
--Procedure ComputeAverageWeightedScoreForUsers is not taking any input.
--Calculate-Weighted-Average
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weights INT;

    -- Compute the total weighted score for all users
    SELECT SUM(score * weight) INTO total_weighted_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id;

    -- Compute the total weights
    SELECT SUM(weight) INTO total_weights
    FROM projects;

    -- Calculate the average weighted score (rounded to 2 decimal places)
    SET @average_weighted_score := ROUND(total_weighted_score / total_weights, 2);

    -- Update all users' average scores
    UPDATE users
    SET average_score = @average_weighted_score;
END;

$$
DELIMITER ;
