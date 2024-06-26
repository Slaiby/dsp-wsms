from datetime import datetime

def generate_html_from_expectations(data, output_file_path):
    html_template = '''
    <!DOCTYPE html>
    <html>
      <head>
        <title>Data documentation compiled by Great Expectations</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://unpkg.com/bootstrap-table@1.19.1/dist/bootstrap-table.min.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" />
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/bootstrap-table@1.19.0/dist/extensions/filter-control/bootstrap-table-filter-control.css">
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/css/bootstrap-datepicker.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@forevolve/bootstrap-dark@1.1.0/dist/css/bootstrap-prefers-dark.css" />
        <style>
          body {{
            position: relative;
          }}

          .container {{
            padding-top: 50px;
          }}

          .sticky {{
            position: -webkit-sticky;
            position: sticky;
            top: 90px;
            z-index: 1;
          }}

          .ge-section {{
            clear: both;
            margin-bottom: 30px;
            padding-bottom: 20px;
          }}

          .popover {{
            max-width: 100%;
          }}

          .cooltip {{
            display: inline-block;
            position: relative;
            text-align: left;
            cursor: pointer;
          }}

          .cooltip .top {{
            min-width: 200px;
            top: -6px;
            left: 50%;
            transform: translate(-50%, -100%);
            padding: 10px 20px;
            color: #FFFFFF;
            background-color: #222222;
            font-weight: normal;
            font-size: 13px;
            border-radius: 8px;
            position: absolute;
            z-index: 99999999 !important;
            box-sizing: border-box;
            box-shadow: 0 1px 8px rgba(0, 0, 0, 0.5);
            display: none;
          }}

          .cooltip:hover .top {{
            display: block;
            z-index: 99999999 !important;
          }}

          .cooltip .top i {{
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -12px;
            width: 24px;
            height: 12px;
            overflow: hidden;
          }}

          .cooltip .top i::after {{
            content: '';
            position: absolute;
            width: 12px;
            height: 12px;
            left: 50%;
            transform: translate(-50%, -50%) rotate(45deg);
            background-color: #222222;
            box-shadow: 0 1px 8px rgba(0, 0, 0, 0.5);
          }}

          ul {{
            padding-inline-start: 20px;
          }}

          .show-scrollbars {{
            overflow: auto;
          }}

          td .show-scrollbars {{
            max-height: 80vh;
          }}

          .show-scrollbars::-webkit-scrollbar {{
            -webkit-appearance: none;
          }}

          .show-scrollbars::-webkit-scrollbar:vertical {{
            width: 11px;
          }}

          .show-scrollbars::-webkit-scrollbar:horizontal {{
            height: 11px;
          }}

          .show-scrollbars::-webkit-scrollbar-thumb {{
            border-radius: 8px;
            border: 2px solid white;
            background-color: rgba(0, 0, 0, .5);
          }}

          footer {{
            position: fixed;
            border-top: 1px solid #98989861;
            bottom: 0;
            left: 0;
            right: 0;
            height: 32px;
            padding: 4px;
            font-size: 14px;
            text-align: right;
            width: 100%;
            background: white;
            z-index: 100000;
          }}
          footer a {{
            padding-right: 8px;
            color: #ff6210;
            font-weight: 600;
          }}
          footer a:hover {{
            color: #bc490d;
            text-decoration: underline;
          }}
          @media (prefers-color-scheme: dark) {{
            .table {{
              color: #f1f1f1 !important;
              background-color: #212529;
            }}
            .table-bordered{{
              border: #f1f1f1;
            }}
            .table-hover tbody tr:hover {{
              color: #f1f1f1;
              background-color: rgba(255,255,255,.075);
            }}
            .form-control:disabled,
            .form-control[readonly]{{
              background-color: #343a40;
              opacity: .8;
            }}
            .bg-light {{
              background: inherit !important;
            }}
            .code-snippet {{
              background: #CDCDCD !important;
            }}
            .alert-secondary a {{
              color: #0062cc;
            }}
            .alert-secondary a:focus, .alert-secondary a:hover{{
              color: #004fa5;
            }}
            .navbar-brand a {{
              background: url('https://great-expectations-web-assets.s3.us-east-2.amazonaws.com/full_logo_dark.png') 0 0 no-repeat;
              background-size: 228.75px 50px;
              display: inline-block
            }}
            .navbar-brand a img {{
              visibility:hidden
            }}
            footer {{
              border-top: 1px solid #ffffff61;
              background: black;
              z-index: 100000;
            }}
            footer a {{
              color: #ff6210;
            }}
            footer a:hover {{
              color: #ff6210;
            }}
          }}
        </style>
      </head>
      <body>
        <nav class="navbar navbar-expand-md sticky-top border-bottom" style="height: 70px">
          <div class="mr-auto">
            <nav class="d-flex align-items-center">
              <div class="float-left navbar-brand m-0 h-100">
                <a href="#">
                  <img
                    class="NO-CACHE"
                    src="https://great-expectations-web-assets.s3.us-east-2.amazonaws.com/logo-long.png"
                    alt="Great Expectations"
                    style="width: auto; height: 50px"
                  />
                </a>
              </div>
            </nav>
          </div>
        </nav>
        <div class="container-fluid pt-4 pb-4 pl-5 pr-5">
          <div class="row">
            <div class="col-lg-2 col-md-2 col-sm-12 d-sm-block px-0">
              <div class="mb-4">
                <div class="col-12 p-0">
                  <p>
                    Data Docs autogenerated using
                    <a href="https://greatexpectations.io">Great Expectations</a>.
                  </p>
                </div>
              </div>
              <div class="sticky">
                <div class="card mb-3">
                  <div class="card-header p-2">
                    <strong>Actions</strong>
                  </div>
                  <div class="card-body p-3">
                    <div class="mb-2">
                      <div class="d-flex justify-content-center">
                        <button type="button" class="btn btn-info" data-toggle="modal" data-target=".ge-walkthrough-modal">
                          Show Walkthrough
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-10 col-lg-10 col-xs-12 pl-md-4 pr-md-3">
              <div id="section-1" class="ge-section container-fluid mb-1 pb-1 pl-sm-3 px-0">
                <div class="row">
                  <div id="section-1-content-block-1" class="col-12">
                    <div id="section-1-content-block-1-header" class="alert alert-secondary">
                      <div>
                        <h5 class="m-0"> Overview </h5>
                      </div>
                    </div>
                  </div>
                  <div id="section-1-content-block-2" class="col-12 table-responsive mt-1">
                    <div id="section-1-content-block-2-header">
                      <div>
                        <h6 class="m-0"> Info </h6>
                      </div>
                    </div>
                    <table id="section-1-content-block-2-body" class="table table-sm" style="margin-bottom:0.5rem !important; margin-top:0.5rem !important;" data-toggle="table">
                      <thead hidden>
                        <tr>
                          <th></th>
                          <th></th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td id="section-1-content-block-2-cell-1-1">
                            <div class="show-scrollbars">Expectation Suite Name</div>
                          </td>
                          <td id="section-1-content-block-2-cell-1-2">
                            <div class="show-scrollbars">{expectation_suite_name}</div>
                          </td>
                        </tr>
                        <tr>
                          <td id="section-1-content-block-2-cell-2-1">
                            <div class="show-scrollbars">Great Expectations Version</div>
                          </td>
                          <td id="section-1-content-block-2-cell-2-2">
                            <div class="show-scrollbars">{great_expectations_version}</div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <div id="failed-expectations-container" class="col-12 table-responsive mt-1">
                    <div id="section-1-content-block-3-body" class="table table-sm">
                      <div id="section-1-content-block-3-header">
                        <div>
                          <h6 class="m-0" style="padding: 10px;">Failed Expectations</h6>
                        </div>
                        <div class="d-flex flex-column">{content}</div>
                      </div>
                      <div id="failed-expectations"></div>
                    </div>
                  </div>
                  <div id="section-1-content-block-3" class="col-12 table-responsive mt-1">
                    <div id="section-1-content-block-3-body" class="table table-sm">
                      <div id="section-1-content-block-3-header">
                        <div>
                          <h6 class="m-0"> Notes </h6>
                        </div>
                      </div>
                      <p>This Expectation suite currently contains {evaluated_expectations} total Expectations across {columns_tested} columns.</p>
                    </div>
                  </div>
                </div>
              </div>
              <div id="section-2" class="ge-section container-fluid mb-1 pb-1 pl-sm-3 px-0">
                <div class="row">
                  <div id="section-2-content-block-1" class="col-12">
                    <div id="section-2-content-block-1-header" class="alert alert-secondary">
                      <div>
                        <h5 class="m-0"> Credit_History </h5>
                      </div>
                    </div>
                  </div>
                  <div id="section-2-content-block-2" class="col-12">
                    <ul id="section-2-content-block-2-body">
                      <li>
                        <span> values must belong to this set: <span class="badge badge-secondary">1.0</span>
                          <span class="badge badge-secondary">0.0</span>. </span>
                      </li>
                      <li style="list-style-type:none;">
                        <hr class="mt-1 mb-1"></hr>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div id="section-3" class="ge-section container-fluid mb-1 pb-1 pl-sm-3 px-0">
                <div class="row">
                  <div id="section-3-content-block-1" class="col-12">
                    <div id="section-3-content-block-1-header" class="alert alert-secondary">
                      <div>
                        <h5 class="m-0"> Dependents </h5>
                      </div>
                    </div>
                  </div>
                  <div id="section-3-content-block-2" class="col-12">
                    <ul id="section-3-content-block-2-body">
                      <li>
                        <span> values must belong to this set: <span class="badge badge-secondary">0</span>
                          <span class="badge badge-secondary">1</span>
                          <span class="badge badge-secondary">2</span>
                          <span class="badge badge-secondary">3+</span>. </span>
                      </li>
                      <li style="list-style-type:none;">
                        <hr class="mt-1 mb-1"></hr>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div id="section-4" class="ge-section container-fluid mb-1 pb-1 pl-sm-3 px-0">
                <div class="row">
                  <div id="section-4-content-block-1" class="col-12">
                    <div id="section-4-content-block-1-header" class="alert alert-secondary">
                      <div>
                        <h5 class="m-0"> Education </h5>
                      </div>
                    </div>
                  </div>
                  <div id="section-4-content-block-2" class="col-12">
                    <ul id="section-4-content-block-2-body">
                      <li>
                        <span> values must belong to this set: <span class="badge badge-secondary">Graduate</span>
                          <span class="badge badge-secondary">Not Graduate</span>. </span>
                      </li>
                      <li style="list-style-type:none;">
                        <hr class="mt-1 mb-1"></hr>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div id="section-5" class="ge-section container-fluid mb-1 pb-1 pl-sm-3 px-0">
                <div class="row">
                  <div id="section-5-content-block-1" class="col-12">
                    <div id="section-5-content-block-1-header" class="alert alert-secondary">
                      <div>
                        <h5 class="m-0"> Loan_Status </h5>
                      </div>
                    </div>
                  </div>
                  <div id="section-5-content-block-2" class="col-12">
                    <ul id="section-5-content-block-2-body">
                      <li>
                        <span> values must belong to this set: <span class="badge badge-secondary">Y</span>
                          <span class="badge badge-secondary">N</span>. </span>
                      </li>
                      <li style="list-style-type:none;">
                        <hr class="mt-1 mb-1"></hr>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div id="section-6" class="ge-section container-fluid mb-1 pb-1 pl-sm-3 px-0">
                <div class="row">
                  <div id="section-6-content-block-1" class="col-12">
                    <div id="section-6-content-block-1-header" class="alert alert-secondary">
                      <div>
                        <h5 class="m-0"> Married </h5>
                      </div>
                    </div>
                  </div>
                  <div id="section-6-content-block-2" class="col-12">
                    <ul id="section-6-content-block-2-body">
                      <li>
                        <span> values must belong to this set: <span class="badge badge-secondary">Yes</span>
                          <span class="badge badge-secondary">No</span>. </span>
                      </li>
                      <li style="list-style-type:none;">
                        <hr class="mt-1 mb-1"></hr>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div id="section-7" class="ge-section container-fluid mb-1 pb-1 pl-sm-3 px-0">
                <div class="row">
                  <div id="section-7-content-block-1" class="col-12">
                    <div id="section-7-content-block-1-header" class="alert alert-secondary">
                      <div>
                        <h5 class="m-0"> Property_Area </h5>
                      </div>
                    </div>
                  </div>
                  <div id="section-7-content-block-2" class="col-12">
                    <ul id="section-7-content-block-2-body">
                      <li>
                        <span> values must belong to this set: <span class="badge badge-secondary">Urban</span>
                          <span class="badge badge-secondary">Rural</span>
                          <span class="badge badge-secondary">Semiurban</span>. </span>
                      </li>
                      <li style="list-style-type:none;">
                        <hr class="mt-1 mb-1"></hr>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <div id="section-8" class="ge-section container-fluid mb-1 pb-1 pl-sm-3 px-0">
                <div class="row">
                  <div id="section-8-content-block-1" class="col-12">
                    <div id="section-8-content-block-1-header" class="alert alert-secondary">
                      <div>
                        <h5 class="m-0"> Self_Employed </h5>
                      </div>
                    </div>
                  </div>
                  <div id="section-8-content-block-2" class="col-12">
                    <ul id="section-8-content-block-2-body">
                      <li>
                        <span> values must belong to this set: <span class="badge badge-secondary">Yes</span>
                          <span class="badge badge-secondary">No</span>. </span>
                      </li>
                      <li style="list-style-type:none;">
                        <hr class="mt-1 mb-1"></hr>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <footer>
          <p>Stay current on everything GX with our newsletter <a href="https://greatexpectations.io/newsletter?utm_source=datadocs&utm_medium=product&utm_campaign=newsletter&utm_content=form">Subscribe</a></p>
        </footer>
      </body>
    </html>
    '''

    content = ""
    results = data.get("results", [])

    for result in results:
        if not result.get("success"):
            column = result.get("expectation_config", {}).get("kwargs", {}).get("column", "Unknown")
            partial_unexpected_list = result.get("result", {}).get("partial_unexpected_list", [])
            unexpected_values = ", ".join(map(str, partial_unexpected_list))
            content += f'''
                  <div class="card mb-3">
                    <div class="card-body">
                        <h6 class="card-title">Column: {column}</h6>
                        <p class="card-text">Unexpected Values: {unexpected_values}</p>
                    </div>
                </div>
            '''

    expectation_suite_name = data.get("meta", {}).get("expectation_suite_name", "N/A")
    great_expectations_version = data.get("meta", {}).get("great_expectations_version", "N/A")
    evaluated_expectations = len(results)
    columns_tested = len(set(result.get("expectation_config", {}).get("kwargs", {}).get("column", "Unknown") for result in results))
    results = data.get('results', [])

    html_content = html_template.format(
        content=content,
        expectation_suite_name=expectation_suite_name,
        great_expectations_version=great_expectations_version,
        evaluated_expectations=evaluated_expectations,
        columns_tested=columns_tested
    )

    html_content = html_template.format(
        content=content,
        expectation_suite_name=expectation_suite_name,
        great_expectations_version=great_expectations_version,
        evaluated_expectations=evaluated_expectations,
        columns_tested=columns_tested
    )

    with open(output_file_path, "w") as file:
        file.write(html_content)
    return output_file_path
