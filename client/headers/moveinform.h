#ifndef MOVEINFORM_H
#define MOVEINFORM_H

#include <QWidget>

#include "baseform.h"

namespace Ui {
class MoveInForm;
}

class MoveInForm : public QWidget, public BaseForm
{
    Q_OBJECT

public:
    explicit MoveInForm(QWidget *parent = nullptr);
    ~MoveInForm();

    void clear() override;

signals:
    void sendData(const QString &data);

private slots:
    void on_moveInBtn_clicked();

private:
    Ui::MoveInForm *ui;
};

#endif // MOVEINFORM_H
