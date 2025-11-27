from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    main_heading = "Deploying an Application on ECS EC2 using AWS CodePipeline"
    secondary_heading = "This is an AWS ECS EC2 deployment with Application Load Balancer and CodePipeline."
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Deployment Status</title>
    </head>
    <body>
        <h1>{main_heading}</h1>
        <h2>{secondary_heading}</h2>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)