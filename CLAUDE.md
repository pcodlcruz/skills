# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Personal repository of Skills ("Repositorio personal de Skills", per README.md). The repository is currently empty apart from the README: there is no build system, linter, test suite or established directory layout yet.

## Conventions

- Each skill should live in its own directory with a `SKILL.md` file at its root. The file starts with YAML frontmatter containing `name` and `description`. The `description` decides when the skill triggers, so list the concrete phrases users will say.
- Supporting material (reference docs, scripts, templates) goes inside the skill's own directory, and `SKILL.md` points to it.
- Branches: `main` is the default branch and `develop` is the working branch.

Update this file once real structure, tooling or validation scripts are added.
