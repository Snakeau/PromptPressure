# Homebrew Formula for PromptPressure
# To use: create repo Snakeau/homebrew-tap, place this file in Formula/
# Users install via: brew install snakeau/tap/promptpressure

class Promptpressure < Formula
  include Language::Python::Virtualenv

  desc "Pressure-test your AI before attackers do. Red-teaming scanner for LLM agents."
  homepage "https://github.com/Snakeau/PromptPressure"
  url "https://files.pythonhosted.org/packages/source/p/promptpressure/promptpressure-0.1.1.tar.gz"
  sha256 "REPLACE_WITH_ACTUAL_SHA256"
  license "MIT"

  depends_on "python@3.12"

  resource "typer" do
    url "https://files.pythonhosted.org/packages/source/t/typer/typer-0.12.5.tar.gz"
    sha256 "REPLACE_WITH_ACTUAL_SHA256"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-13.9.4.tar.gz"
    sha256 "REPLACE_WITH_ACTUAL_SHA256"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/source/r/requests/requests-2.32.3.tar.gz"
    sha256 "REPLACE_WITH_ACTUAL_SHA256"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "promptpressure", shell_output("#{bin}/promptpressure --version")
  end
end

# Setup instructions:
#
# 1. Create GitHub repo: Snakeau/homebrew-tap
# 2. Create directory: Formula/
# 3. Place this file as: Formula/promptpressure.rb
# 4. Replace SHA256 hashes with actual values:
#    - pip download promptpressure==0.1.1 --no-deps --no-binary :all:
#    - shasum -a 256 promptpressure-0.1.1.tar.gz
#    - Do the same for each resource (typer, rich, requests)
# 5. Users install via:
#    brew tap snakeau/tap
#    brew install promptpressure
