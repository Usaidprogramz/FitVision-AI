# FitVision AI -- Team Contributions

## Purpose

Record team responsibilities and development contributions. Update this
document as tasks are assigned, completed, reviewed, and merged.

## Team Structure

  -----------------------------------------------------------------------
  Team member             Main responsibility     GitHub branch
  ----------------------- ----------------------- -----------------------
  Project owner           Bicep-curl prototype,   `feature/bicep-curl`
                          integration,            
                          coordination            

  Friend 1                Squat exercise module   `feature/squat`

  Friend 2                Push-up exercise module `feature/push-up`
  -----------------------------------------------------------------------

Replace role labels with team members' preferred names or GitHub
usernames if the team agrees. Lunge implementation can be assigned
later.

## Branching Workflow

-   Keep `main` as the stable integration branch.
-   Each member works on their own feature branch.
-   Avoid committing unfinished work directly to `main`.
-   Push completed work to the matching feature branch.
-   Open a pull request from the feature branch into `main`.
-   Review and test changes before merging.

## Contribution Record

Add a row whenever a meaningful task is completed.

  ----------------------------------------------------------------------------------
  Date           Contributor    Task           Branch / Pull request  Status
  -------------- -------------- -------------- ---------------------- --------------
  YYYY-MM-DD     Project owner  Initial        `feature/bicep-curl`   In progress
                                bicep-curl                            
                                prototype                             

  YYYY-MM-DD     Friend 1       Squat module   `feature/squat`        Not started

  YYYY-MM-DD     Friend 2       Push-up module `feature/push-up`      Not started
  ----------------------------------------------------------------------------------

Suggested statuses: `Not started`, `In progress`, `In review`, and
`Completed`.

## Team Working Rules

1.  Pull the latest `main` before starting a new task.
2.  Work mainly inside the folder assigned to your exercise.
3.  Avoid editing the same files simultaneously.
4.  Use clear commit messages.
5.  Test changes before opening a pull request.
6.  Explain important changes in the pull request description.
7.  Discuss shared architecture or dependency changes with the team.
8.  Never commit passwords, API keys, private data, or unapproved
    participant recordings.

## Pull Request Checklist

-   [ ] Code is related to the assigned task.
-   [ ] Code runs without known errors.
-   [ ] Relevant tests or manual checks have been performed.
-   [ ] No unnecessary files or private data are included.
-   [ ] Documentation has been updated where necessary.
-   [ ] Pull request explains what changed and how it was tested.

## Meeting Notes

Record decisions, blockers, and next actions in separate files inside
`docs/meeting_notes/`. Example filename:

``` text
docs/meeting_notes/2026-11-01.md
```
