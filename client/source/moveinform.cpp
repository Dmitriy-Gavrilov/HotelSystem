#include "moveinform.h"
#include "ui_moveinform.h"

MoveInForm::MoveInForm(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::MoveInForm)
{
    ui->setupUi(this);
}

MoveInForm::~MoveInForm()
{
    delete ui;
}

void MoveInForm::clear()
{
    this->ui->passport->clear();
    this->ui->roomId->clear();
    this->ui->dateMoveIn->setDate(QDate::fromString("01.01.2024", "dd.MM.yyyy"));
    this->ui->dateDepart->setDate(QDate::fromString("01.01.2024", "dd.MM.yyyy"));
}

void MoveInForm::on_moveInBtn_clicked()
{
    QString data = "moveIn;" + this->ui->roomId->text() + ";" + this->ui->passport->text() + ";" +
                   this->ui->dateMoveIn->text() + ";" + this->ui->dateDepart->text();
    emit sendData(data);
}

