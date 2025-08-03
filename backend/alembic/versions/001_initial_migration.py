"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('campaigns',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('companies',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('campaign_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('domain', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('people',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    
    op.create_table('context_snippets',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('entity_type', sa.String(), nullable=False),
    sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('snippet_type', sa.String(), nullable=True),
    sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('source_urls', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("entity_type IN ('company', 'person')", name='valid_entity_type'),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('search_logs',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('context_snippet_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('iteration', sa.Integer(), nullable=True),
    sa.Column('query', sa.String(), nullable=True),
    sa.Column('top_results', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['context_snippet_id'], ['context_snippets.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('search_logs')
    op.drop_table('context_snippets')
    op.drop_table('people')
    op.drop_table('companies')
    op.drop_table('campaigns')