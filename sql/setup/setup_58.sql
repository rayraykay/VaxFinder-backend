




CREATE procedure [dbo].[vaccine_availability_requirements_Delete] 
(
	@id uniqueidentifier,
	@auth uniqueidentifier
)
AS
	SET NOCOUNT ON;

	BEGIN TRY

		BEGIN TRANSACTION;

			declare @valid bit
			declare @location int
			
			select @location = vaccine_availability.location from dbo.vaccine_availability join dbo.vaccine_availability_requirements on vaccine_availability_requirements.vaccine_availability = vaccine_availability.id where vaccine_availability_requirements.id = @id

			select @valid = dbo.ValidateLocationKey(@auth, @location)

			if @valid = 0
			BEGIN
				return(0);
			END
			
			delete from vaccine_availability_requirements where id = @id

		COMMIT TRANSACTION;
		
		RETURN(1);

	END TRY

	BEGIN CATCH

-- ==== Rollback transaction
		IF XACT_STATE() <> 0
			ROLLBACK TRANSACTION;

		RETURN(-1);

	END CATCH