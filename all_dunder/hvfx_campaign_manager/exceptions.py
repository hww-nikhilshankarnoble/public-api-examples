"""
Exceptions for the hvfx_campaign_manager package.
"""

__all__ = ["CampaignDirectoryDoesNotExist"]


class GitError(Exception):
    """
    Raised when a Git command errors.
    """


class CampaignDirectoryDoesNotExist(Exception):
    """
    Raised when the campaign directory does not exist.
    """
