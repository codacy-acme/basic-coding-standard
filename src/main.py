"""Main script for creating a Codacy coding standard."""
import sys
import click
from typing import Optional
from src.api.codacy import CodacyAPI
from src.utils.logger import setup_logger

def process_patterns(
    api: CodacyAPI,
    logger: any,
    standard_id: str,
    tool_uuid: str,
    dry_run: bool
) -> None:
    """
    Process patterns for a tool, disabling minor findings.
    
    Args:
        api: CodacyAPI instance
        logger: Logger instance
        standard_id: Coding standard ID
        tool_uuid: Tool UUID
        dry_run: Whether to run in dry-run mode
    """
    patterns = api.get_patterns(standard_id, tool_uuid)
    patterns_to_update = []
    
    for pattern in patterns:
        pattern_def = pattern.get('patternDefinition', {})
        pattern_id = pattern_def.get('id')
        severity = pattern_def.get('severityLevel', '').lower()
        
        if severity in ['info', 'minor']:
            patterns_to_update.append({
                'id': pattern_id,
                'enabled': False
            })
            if dry_run:
                logger.info(
                    f"[DRY RUN] Would disable pattern: {pattern_id} "
                    f"({severity})"
                )
    
    if patterns_to_update and not dry_run:
        # Update patterns in batches of 500 to avoid request size limits
        for i in range(0, len(patterns_to_update), 500):
            batch = patterns_to_update[i:i + 500]
            api.update_patterns(standard_id, tool_uuid, batch)
            logger.info(f"Disabled {len(batch)} minor patterns")

def create_standard(
    project_name: str,
    dry_run: bool = False,
    verbose: bool = False,
    output: Optional[str] = None
) -> None:
    """
    Create a new coding standard with all languages and tools enabled,
    but minor findings disabled.
    
    Args:
        project_name: Name for the new coding standard
        dry_run: Whether to preview changes without applying them
        verbose: Whether to enable verbose logging
        output: Optional custom log file path
    """
    logger = setup_logger(output, verbose)
    api = CodacyAPI()
    
    try:
        # Create new coding standard
        logger.info(f"Creating new coding standard: {project_name}")
        if dry_run:
            logger.info("[DRY RUN] Would create new coding standard")
            standard_id = "dry-run-id"
        else:
            response = api.create_coding_standard(project_name)
            standard_id = response.get("data", {}).get("id")
            if not standard_id:
                raise ValueError("Failed to get coding standard ID from response")
            logger.info(f"Created coding standard with ID: {standard_id}")

        # Get and enable all tools
        logger.info("Fetching available tools...")
        tools = api.get_available_tools()
        
        if not tools:
            logger.warning("No tools found")
            return
            
        for tool in tools:
            try:
                tool_uuid = tool.get('uuid')
                tool_name = tool.get('name')
                
                if not tool_uuid or not tool_name:
                    logger.warning(f"Skipping tool with incomplete data: {tool}")
                    continue
                    
                logger.info(f"Processing tool: {tool_name}")
                
                if not dry_run:
                    # Enable the tool
                    api.enable_tool(standard_id, tool_uuid)
                    logger.info(f"Enabled tool: {tool_name}")
                    
                    # Process patterns
                    process_patterns(api, logger, standard_id, tool_uuid, dry_run)
                else:
                    logger.info(f"[DRY RUN] Would enable tool: {tool_name}")
                    process_patterns(api, logger, standard_id, tool_uuid, dry_run)
                    
            except Exception as e:
                logger.error(f"Error processing tool {tool_name}: {str(e)}")
                continue

        if not dry_run:
            # Promote the coding standard
            logger.info("Promoting coding standard...")
            api.promote_draft(standard_id)
            
            # Set as default
            logger.info("Setting as default coding standard...")
            api.set_default(standard_id)

        logger.info("Successfully created and configured coding standard")
        
    except Exception as e:
        logger.error(f"Failed to create coding standard: {str(e)}")
        sys.exit(1)

@click.command()
@click.option(
    "--project-name",
    required=True,
    help="Name for the new coding standard"
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Preview changes without applying them"
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging"
)
@click.option(
    "--output",
    type=str,
    help="Custom log file path"
)
def main(
    project_name: str,
    dry_run: bool,
    verbose: bool,
    output: Optional[str]
) -> None:
    """Create a Codacy coding standard with all languages and tools enabled."""
    create_standard(project_name, dry_run, verbose, output)

if __name__ == "__main__":
    main()
