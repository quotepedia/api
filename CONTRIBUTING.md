# Contributing to Quotepedia API

> [!CAUTION]
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project license.

Thank you for contributing!

Every contribution is welcome. First, please read the relevant section before contributing to ensure a smooth process for everyone. The community appreciates your support!

> In case if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
>
> - Star the project
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends or colleagues

## I have a Question

Before you ask a question, it's best to search for existing [issues](https://github.com/quotepedia/api/issues). In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [issue](https://github.com/quotepedia/api/issues/new) with corresponding tags.
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (python, pdm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

## Reporting Bugs

> [!WARNING]
> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be sent to organization members.

We use issues to track bugs and errors. When experiencing issues with this project, please open a [bug report issue](https://github.com/quotepedia/api/issues/new?template=bug_report.yaml).

Once it's submitted:

- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs with the `needs-repro` tag will not be addressed until they are reproduced.
- If the team is able to reproduce the issue, it will be marked `needs-fix`, as well as possibly other tags (such as `critical`), and the issue will be left to be [implemented by someone](#code-contribution).

## Requesting Features

> [!NOTE]
> Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on.

We use issues to track feature requests. To suggest an enhancement, please open a [feature request issue](https://github.com/quotepedia/api/issues/new?template=feature_request.yaml).

Once it's submitted:

- Our team will review and discuss your suggestion.

## Code Contribution

### Prerequisites

- [**Python**](https://www.python.org/downloads/): Ensure you have the required minimum version specified in the [`pyproject.toml`](pyproject.toml).
- [**PDM**](https://pdm-project.org/): This project uses **pdm instead of pip** for convenient scripts and dependency management.
- [**PostgreSQL**](https://www.postgresql.org/download): Set up and create a PostgreSQL database for data storage.
- [**Redis**](https://redis.io/download): Start a new redis service for caching and data storage.
- **SMTP Server**: Set up an SMTP server for mailings.

### Submitting PRs

If you encounter any issues or are unsure about what to work on, please search for "TODO" comments in the project code. These comments indicate tasks that need to be completed. For example, you might find something like this:

```python
# TODO: Optimize this function to improve performance and reduce execution time.
```

These notes can guide you on areas that require attention or improvement.

#### Step 1 — Clone the repository

To start contributing to the project, fork it first and then clone your fork to your local machine using git:

- Clone using the web URL:
  ```sh
  git clone https://github.com/quotepedia/api.git
  ```
- Use a password-protected SSH key:
  ```sh
  git clone git@github.com:quotepedia/api.git
  ```
- Work with official GitHub CLI:
  ```sh
  gh repo clone quotepedia/api
  ```

#### Step 2 — Configure environment

Create a [`config.yaml`](config.yaml) file in the project root directory and populate it based on the example in [`config.sample.yaml`](config.sample.yaml).

Then, run the following commands to set up your environment:

```sh
pdm install
pdm i18n:compile
pdm run alembic upgrade head
```

#### Step 3 — Make changes

> [!IMPORTANT]
> Please adhere to the code style used throughout the project.

Contributions can vary from simple [`README.md`](README.md) updates to bug fixes or new features. Depending on the nature of your contribution, you may need to follow additional steps outlined below. Focus on the updates you wish to merge into this repository.

#### Step 4 — Write tests

We strive to maintain comprehensive test coverage in our codebase. All the tests are located in the [`tests`](tests/) folder.

#### Step 5 — Update documentation

We recommend you to review the [`README.md`](README.md) and look for anything needs to be updated regarding the changes you made.

#### Step 6 — Commit changes

Before committing your changes, run these scripts to ensure everything is fine:

```sh
pdm format
pdm check
pdm test
```

#### Step 7 — Submit a pull request

Once you are satisfied with your changes: [submit a pull request](https://github.com/quotepedia/api/compare).

Your efforts help improve the project for everyone!

### Commit Messages

We're following the [Conventional Commits](https://www.conventionalcommits.org) specification for adding human and machine readable meaning to commit messages.

## Localization

We utilize [gettext](https://www.gnu.org/software/gettext/) for internationalization (i18n) purposes in our API. This approach enables us to create high-quality client apps that can localize error messages out of the box.

### Supported Languages

- English ([en](src/i18n/locales/en/))
- Russian ([ru](src/i18n/locales/ru/))

You can find a complete list of all supported locales [here](src/i18n/locales). For editing we recommend using [Poedit](https://poedit.net/) as a GUI.

### Scripts

We have three main i18n scripts defined in [`pyproject.toml`](pyproject.toml) that leverage [Babel's CLI](https://babel.pocoo.org) to manipulate translation messages:

- **Extract**: Creates `messages.pot` (Portable Object Template) using methods defined in [`pyproject.toml`](pyproject.toml):
  ```sh
  pdm i18n:extract
  ```
- **Update**: Modifies `messages.po` (Portable Object) for each locale that is sent to translators:
  ```sh
  pdm i18n:update
  ```
- **Compile**: Generates `messages.mo` (Machine Object) for each locale that is used at runtime:
  ```sh
  pdm i18n:compile
  ```

## Join The Project Team

Contact the organization members in order to join the project team.
