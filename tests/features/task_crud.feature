Feature: Task management
  As a Vikunja user
  I want to create, rename, complete and delete tasks
  So that my task list reflects what I need to do

  Scenario: Create a task
    Given I am on my task list
    When I add a task with a unique title
    Then the task appears in my task list

  Scenario: Rename a task
    Given a task exists
    When I rename the task
    Then the new title is still shown after a reload

  Scenario: Complete a task
    Given a task exists
    And I am on my task list
    And the task is not done
    When I mark the task as done
    Then the task is marked as done

  Scenario: Delete a task
    Given a task exists
    When I delete the task
    Then the task no longer exists