

CREATE FUNCTION [dbo].[ValidateAdminKey](@key uniqueidentifier)
RETURNS bit AS
BEGIN
    declare @role int
	select @role = [role] from dbo.keys where id = @key

	IF @role = 1
	BEGIN
		RETURN 1
	END

	RETURN 0
END