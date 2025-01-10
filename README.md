<div align="center">
  <img src="https://images.weserv.nl/?url=https://github.com/myceliumAI/mycelium/blob/main/mycelium/src/assets/logo.png?raw=true&fit=cover&mask=circle&maxage=7d" alt="Mycelium Logo" width="150"/>
  <br><br>
  
  <div>
    <kbd><h1 align="center">[ MYCELIUM ]</h1></kbd>
    <br><br>
    <table align="center">
      <tr>
        <td align="left"><code>[LICENSE]</code></td>
        <td>
          <a href="https://www.gnu.org/licenses/agpl-3.0">
            <img src="https://img.shields.io/badge/License-AGPL_v3-blue.svg" alt="License: AGPL v3"/>
          </a>
        </td>
      </tr>
      <tr>
        <td align="left"><code>[METRICS]</code></td>
        <td>
          <a href="https://github.com/ThomasGraff/mycelium/stargazers">
            <img src="https://img.shields.io/github/stars/ThomasGraff/mycelium.svg" alt="GitHub Stars"/>
          </a>
          <a href="https://github.com/ThomasGraff/mycelium/network">
            <img src="https://img.shields.io/github/forks/ThomasGraff/mycelium.svg" alt="GitHub Forks"/>
          </a>
          <a href="https://github.com/ThomasGraff/mycelium/issues">
            <img src="https://img.shields.io/github/issues/ThomasGraff/mycelium.svg" alt="GitHub Issues"/>
          </a>
        </td>
      </tr>
      <tr>
        <td align="left"><code>[UTILS]</code></td>
        <td>
          <a href="#documentation">
            <code>DOCS</code>
          </a>
          &nbsp;&nbsp;|&nbsp;&nbsp;
          <a href="https://github.com/ThomasGraff/mycelium/issues/new?template=bug_report.md">
            <code>BUGS</code>
          </a>
          &nbsp;&nbsp;|&nbsp;&nbsp;
          <a href="https://github.com/ThomasGraff/mycelium/issues/new?template=feature_request.md">
            <code>FEATURES</code>
          </a>
        </td>
      </tr>
      <tr>
        <td align="left"><code>[DESCRIPTION]</code></td>
        <td><i>
          A powerful platform designed to simplify the creation and management<br>
          of Data Contracts, bridging systems for seamless data ingestion.</i>
        </td>
      </tr>
    </table>
  </div>
</div>

<div align="center">│</div>
<div align="center">▼</div>
<br>
<div align="center">
  <div>
    <kbd><h2 align="center">[ CORE_FEATURES ]</h2></kbd>
    <br><br>
    <table>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/artificial-intelligence.png" width="30"/>
          <br />
          <b><span style="color: #00ff00;">></span> AI-Powered Contracts</b>
          <br />
          Auto-generate data contracts using advanced LLM technology
        </td>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/speed.png" width="30"/>
          <br />
          <b><span style="color: #00ff00;">></span> Fast Ingestion</b>
          <br />
          Automated configuration and streamlined pipeline setup
        </td>
      </tr>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/dashboard.png" width="30"/>
          <br />
          <b><span style="color: #00ff00;">></span> Smart Visualization</b>
          <br />
          Track contracts and map data sources in real-time
        </td>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/collaboration.png" width="30"/>
          <br />
          <b><span style="color: #00ff00;">></span> Team Collaboration</b>
          <br />
          Unite teams with centralized contract management
        </td>
      </tr>
    </table>
  </div>
</div>

<div align="center">│</div>
<div align="center">▼</div>
<br>
<div align="center">
  <div>
    <kbd><h2 align="center">[ DEPENDENCY_CHECK ]</h2></kbd>
    <br><br>
    <table>
      <tr>
        <td align="center" width="50%">
          <img src="https://img.icons8.com/color/48/000000/docker.png" width="30"/>
          <br />
          <b>Production</b>
          <br />
          <code>make check-prod</code>
        </td>
        <td align="center" width="50%">
          <img src="https://img.icons8.com/color/48/000000/code.png" width="30"/>
          <br />
          <b>Development</b>
          <br />
          <code>make check-dev</code>
        </td>
      </tr>
    </table>
  </div>
</div>

<div align="center">│</div>
<div align="center">▼</div>
<br>
<div align="center">
  <div>
    <kbd><h2 align="center">[ ENVIRONMENT_SETUP ]</h2></kbd>
    <br><br>
    <table>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/settings.png" width="30"/>
          <br />
          <code>make setup</code>
        </td>
      </tr>
    </table>
    <details>
      <summary>
        <b>click to view configuration details</b>
      </summary>
      <br>
      <table>
        <tr>
          <th>Variable</th>
          <th>Default</th>
          <th>Description</th>
        </tr>
        <tr>
          <th colspan="3" align="center">Global Backend Configuration</th>
        </tr>
        <tr>
          <td><code>BACKEND_HOST</code></td>
          <td>localhost</td>
          <td>Hostname for the backend service in the Docker network</td>
        </tr>
        <tr>
          <th colspan="3" align="center">API Configuration</th>
        </tr>
        <tr>
          <td><code>API_PORT</code></td>
          <td>8000</td>
          <td>Port on which the FastAPI backend service will listen</td>
        </tr>
        <tr>
          <th colspan="3" align="center">Database Configuration</th>
        </tr>
        <tr>
          <td><code>POSTGRES_USER</code></td>
          <td>admin</td>
          <td>PostgreSQL username for database authentication</td>
        </tr>
        <tr>
          <td><code>POSTGRES_PASSWORD</code></td>
          <td>(generated)</td>
          <td>PostgreSQL password for database authentication</td>
        </tr>
        <tr>
          <td><code>POSTGRES_PORT</code></td>
          <td>5432</td>
          <td>Port number for PostgreSQL database connection</td>
        </tr>
        <tr>
          <td><code>POSTGRES_DB</code></td>
          <td>mycelium_db</td>
          <td>Name of the PostgreSQL database</td>
        </tr>
        <tr>
          <th colspan="3" align="center">Keycloak Configuration</th>
        </tr>
        <tr>
          <td><code>KC_BOOTSTRAP_ADMIN_USERNAME</code></td>
          <td>admin</td>
          <td>Keycloak administrator username</td>
        </tr>
        <tr>
          <td><code>KC_BOOTSTRAP_ADMIN_PASSWORD</code></td>
          <td>(generated)</td>
          <td>Keycloak administrator password</td>
        </tr>
        <tr>
          <td><code>KC_PORT</code></td>
          <td>8081</td>
          <td>Port number for Keycloak server</td>
        </tr>
        <tr>
          <td><code>KC_MANAGEMENT_PORT</code></td>
          <td>9000</td>
          <td>Keycloak management port</td>
        </tr>
        <tr>
          <td><code>KC_REALM</code></td>
          <td>mycelium</td>
          <td>Name of the Keycloak realm</td>
        </tr>
        <tr>
          <td><code>KC_CLIENT_ID</code></td>
          <td>(generated)</td>
          <td>Client ID for Keycloak authentication</td>
        </tr>
        <tr>
          <th colspan="3" align="center">Frontend Configuration</th>
        </tr>
        <tr>
          <td><code>FRONTEND_PORT</code></td>
          <td>8080</td>
          <td>Port on which the Vue.js frontend will be served</td>
        </tr>
        <tr>
          <td><code>FRONTEND_HOST</code></td>
          <td>localhost</td>
          <td>Hostname for the frontend service in the Docker network</td>
        </tr>
        <tr>
          <td><code>NGINX_LOG_LEVEL</code></td>
          <td>error</td>
          <td>Logging level for Nginx reverse proxy</td>
        </tr>
      </table>
    </details>
  </div>
</div>

<div align="center">│</div>
<div align="center">▼</div>
<br>
<div align="center">
  <div>
    <kbd><h2 align="center">[ LAUNCHING.. ]</h2></kbd>
    <br><br>
    <table>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/launch-box.png" width="30"/>
          <br>
          <code>make launch</code>
          <br>
        </td>
      </tr>
    </table>
    <details>
      <summary>
        <b>click to view individual service commands</b>
      </summary>
      <br>
      <table>
        <tr>
          <td align="center">
            <img src="https://img.icons8.com/color/48/000000/web.png" width="25"/>
            <br>
            <code>make front</code> or <code>make front-dev</code>
            <br>
            <small>Frontend (Production/Development)</small>
          </td>
          <td align="center">
            <img src="https://img.icons8.com/color/48/000000/api.png" width="25"/>
            <br>
            <code>make back</code> or <code>make back-dev</code>
            <br>
            <small>Backend (Production/Development)</small>
          </td>
        </tr>
        <tr>
          <td align="center">
            <img src="https://img.icons8.com/color/48/000000/docker.png" width="25"/>
            <br>
            <code>make build-front</code>
            <br>
            <small>Build Frontend Docker Image</small>
          </td>
          <td align="center">
            <img src="https://img.icons8.com/color/48/000000/docker.png" width="25"/>
            <br>
            <code>make build-back</code>
            <br>
            <small>Build Backend Docker Images</small>
          </td>
        </tr>
      </table>
    </details>
  </div>
</div>

<div align="center">│</div>
<div align="center">▼</div>
<br>
<div align="center">
  <div>
    <kbd><h2 align="center">[ CLEANING.. ]</h2></kbd>
    <br><br>
    <table>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/delete-forever.png" width="30"/>
          <br>
          <code>make clean</code>
          <br>
        </td>
      </tr>
    </table>
    <details>
      <summary>
        <b>click to view individual cleaning commands</b>
      </summary>
      <br>
      <table>
        <tr>
          <td align="center">
            <img src="https://img.icons8.com/color/48/000000/web.png" width="25"/>
            <br>
            <code>make clean-front</code>
            <br>
            <small>Clean Frontend Docker Resources</small>
          </td>
          <td align="center">
            <img src="https://img.icons8.com/color/48/000000/api.png" width="25"/>
            <br>
            <code>make clean-back</code>
            <br>
            <small>Clean Backend Docker Resources</small>
          </td>
        </tr>
      </table>
    </details>
  </div>
</div>

<div align="center">│</div>
<div align="center">▼</div>
<br>
<div align="center">
  <div>
    <kbd><h2 align="center">[ CONTRIBUTION_PROTOCOL ]</h2></kbd>
    <br><br>
    <table>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/code-fork.png" width="30"/>
          <br />
          <b>Fork</b>
          <br />
          Fork the repository
        </td>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/split.png" width="30"/>
          <br />
          <b>Branch</b>
          <br />
          <code>git checkout -b feat/YourFeature</code>
        </td>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/commit-git.png" width="30"/>
          <br />
          <b>Commit</b>
          <br />
          <code>git commit -m 'Add feature'</code>
        </td>
      </tr>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/upload-to-cloud.png" width="30"/>
          <br />
          <b>Push</b>
          <br />
          <code>git push origin feat/YourFeature</code>
        </td>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/pull-request.png" width="30"/>
          <br />
          <b>Pull Request</b>
          <br />
          Open a PR on GitHub
        </td>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/communication.png" width="30"/>
          <br />
          <b>Discuss</b>
          <br />
          Engage in review process
        </td>
      </tr>
    </table>
  </div>
</div>
