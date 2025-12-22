# Generated migration for adding image field to Announcement model

from django.db import migrations, models


class AddFieldIfNotExists(migrations.AddField):
    """Custom AddField that checks if column exists before adding"""
    
    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model(app_label, self.model_name)
        if self.allow_migrate_model(schema_editor.connection.alias, model):
            # Check if column already exists (database-agnostic)
            with schema_editor.connection.cursor() as cursor:
                db_engine = schema_editor.connection.vendor
                table_name = model._meta.db_table
                column_name = self.name
                
                if db_engine == 'postgresql':
                    # PostgreSQL query
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM information_schema.columns 
                        WHERE table_schema = current_schema()
                        AND table_name = %s 
                        AND column_name = %s
                    """, [table_name, column_name])
                elif db_engine == 'mysql':
                    # MySQL query
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM INFORMATION_SCHEMA.COLUMNS 
                        WHERE TABLE_SCHEMA = DATABASE() 
                        AND TABLE_NAME = %s 
                        AND COLUMN_NAME = %s
                    """, [table_name, column_name])
                else:
                    # SQLite or other - use Django's introspection
                    from django.db import connection
                    columns = [col.name for col in connection.introspection.get_table_description(
                        cursor, table_name
                    )]
                    column_exists = column_name in columns
                    if not column_exists:
                        super().database_forwards(app_label, schema_editor, from_state, to_state)
                    return
                
                column_exists = cursor.fetchone()[0] > 0
                
                if not column_exists:
                    # Only add if it doesn't exist
                    super().database_forwards(app_label, schema_editor, from_state, to_state)


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0020_event_image'),
    ]

    operations = [
        AddFieldIfNotExists(
            model_name='announcement',
            name='image',
            field=models.ImageField(blank=True, help_text='Announcement image', null=True, upload_to='announcements/'),
        ),
    ]

