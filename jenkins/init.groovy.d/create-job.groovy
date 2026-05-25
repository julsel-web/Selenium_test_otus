import jenkins.model.Jenkins
import org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import hudson.model.BooleanParameterDefinition
import hudson.model.ChoiceParameterDefinition
import hudson.model.ParametersDefinitionProperty
import hudson.model.StringParameterDefinition

def jenkins = Jenkins.instance
def jobName = "ui-autotests"
def jobFile = new File("/usr/share/jenkins/ref/jobs/ui-autotests.Jenkinsfile")

if (!jobFile.exists()) {
    println("Pipeline definition file not found: ${jobFile.absolutePath}")
    return
}

def script = jobFile.text
def existingJob = jenkins.getItem(jobName)
def parameterDefinitions = [
    new BooleanParameterDefinition("USE_LOCAL_REPO", true, "Use local repository mounted into Jenkins instead of cloning from GitHub"),
    new StringParameterDefinition("LOCAL_REPO_PATH", "/local-repo", "Mounted local repository path inside Jenkins container"),
    new StringParameterDefinition("GIT_REPO_URL", "https://github.com/julsel-web/Selenium_test_otus.git", "GitHub repository with autotests"),
    new StringParameterDefinition("GIT_BRANCH", "main", "Git branch to checkout"),
    new BooleanParameterDefinition("START_TEST_STACK", true, "Start OpenCart + Selenoid docker-compose stack before tests"),
    new BooleanParameterDefinition("TEARDOWN_TEST_STACK", false, "Stop docker-compose stack after build"),
    new StringParameterDefinition("STACK_COMPOSE_FILE", "/opt/jenkins-stack/opencart-stack/docker-compose.yml", "Path to docker-compose file with OpenCart and Selenoid"),
    new StringParameterDefinition("SELENOID_URL", "http://host.docker.internal:4445/wd/hub", "Remote WebDriver / Selenoid URL"),
    new StringParameterDefinition("APP_URL", "http://host.docker.internal:8082", "Application base URL"),
    new ChoiceParameterDefinition("BROWSER", ["chrome", "firefox"] as String[], "Browser name"),
    new StringParameterDefinition("BROWSER_VERSION", "120.0", "Browser version for Selenoid"),
    new StringParameterDefinition("THREADS", "1", "Parallel test threads for pytest-xdist")
]
def parametersProperty = new ParametersDefinitionProperty(parameterDefinitions)

if (existingJob == null) {
    def job = jenkins.createProject(WorkflowJob, jobName)
    job.definition = new CpsFlowDefinition(script, true)
    job.removeProperty(ParametersDefinitionProperty.class)
    job.addProperty(parametersProperty)
    job.description = "Pipeline for Selenium UI autotests with parametrized Selenoid/App URL/Browser/Version/Threads and Allure HTML report."
    job.save()
    println("Created Jenkins job: ${jobName}")
} else {
    existingJob.definition = new CpsFlowDefinition(script, true)
    existingJob.removeProperty(ParametersDefinitionProperty.class)
    existingJob.addProperty(parametersProperty)
    existingJob.save()
    println("Updated Jenkins job: ${jobName}")
}

jenkins.save()
