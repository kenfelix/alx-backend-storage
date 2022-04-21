-- Creates a stored procedure, ComputeOverallScoreForUser that computes and
-- stores the overall score for a student

DELIMITER //
CREATE PROCEDURE ComputeOverallScoreForUser(
	IN user_id INTEGER
)
BEGIN
	UPDATE users
	SET overall_score = (SELECT AVG(score)
		FROM corrections
		WHERE corrections.user_id=user_id
		GROUP BY corrections.user_id )
	WHERE id=user_id;
END //
DELIMITER;
